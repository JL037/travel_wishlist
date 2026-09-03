"""AT Protocol Phase 2 dual-write orchestration: create/update/delete a
user's PDS records for their wishlist/visited/travel-plan rows, and retry
ones that failed on their first attempt (the outbox pattern from
AT_PROTOCOL_MIGRATION.md section 7).

Every sync_* function here is best-effort and never raises: a PDS write is
not part of the local DB transaction (a local Postgres write and a remote
PDS write can't be made atomic across two systems - see "Failure handling"
in section 7), so on failure we record the error on the row and leave
`atproto_sync_pending` set for a later retry, rather than raising into the
caller. The local write already succeeded by the time these run and must
never be rolled back or blocked on PDS availability - a slow or unreachable
PDS should degrade to "will sync later," not fail the request (see
AT_PROTOCOL_MIGRATION.md section 11, "BYO-PDS reliability").
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.location import VisitedLocation, WishlistLocation
from app.models.travel_plan import TravelPlan
from app.models.users import User
from app.utils.atproto_lexicons import (
    TRAVEL_PLAN_COLLECTION,
    VISITED_LOCATION_COLLECTION,
    WISHLIST_LOCATION_COLLECTION,
    travel_plan_to_record,
    visited_location_to_record,
    wishlist_location_to_record,
)
from app.utils.atproto_repo import create_record, delete_record, get_valid_session, put_record, rkey_from_uri


def _sync_is_active(user: User) -> bool:
    return bool(user.did and user.atproto_sync_enabled)


async def _write_record(db, session, collection: str, record: dict, existing_uri: str | None) -> tuple[str, str]:
    if existing_uri:
        return await put_record(db, session, collection, rkey_from_uri(existing_uri), record)
    return await create_record(db, session, collection, record)


async def sync_wishlist_location(db: AsyncSession, user: User, location: WishlistLocation) -> None:
    if not _sync_is_active(user):
        return
    try:
        session = await get_valid_session(db, user.id)
        record = wishlist_location_to_record(location)
        uri, cid = await _write_record(
            db, session, WISHLIST_LOCATION_COLLECTION, record, location.atproto_record_uri
        )
    except Exception as e:  # noqa: BLE001 - outbox boundary, see module docstring
        location.atproto_sync_pending = True
        location.atproto_sync_error = str(e)
        await db.commit()
        return

    location.atproto_record_uri = uri
    location.atproto_record_cid = cid
    location.atproto_sync_pending = False
    location.atproto_sync_error = None
    await db.commit()


async def sync_visited_location(
    db: AsyncSession, user: User, visited: VisitedLocation, wishlist_location: WishlistLocation | None = None
) -> None:
    if not _sync_is_active(user):
        return

    if wishlist_location is None:
        result = await db.execute(select(WishlistLocation).where(WishlistLocation.id == visited.wishlist_id))
        wishlist_location = result.scalar_one_or_none()
    if wishlist_location is None:
        visited.atproto_sync_pending = True
        visited.atproto_sync_error = "No matching wishlist location to derive city/country from"
        await db.commit()
        return

    # Sync the wishlist record first so this one can carry a strong ref to
    # it, but a wishlist-sync failure shouldn't block this record - it's
    # still valid without wishlistUri, just less linked.
    if not wishlist_location.atproto_record_uri:
        await sync_wishlist_location(db, user, wishlist_location)

    wishlist_ref = None
    if wishlist_location.atproto_record_uri and wishlist_location.atproto_record_cid:
        wishlist_ref = (wishlist_location.atproto_record_uri, wishlist_location.atproto_record_cid)

    try:
        session = await get_valid_session(db, user.id)
        record = visited_location_to_record(visited, wishlist_location, wishlist_ref)
        uri, cid = await _write_record(db, session, VISITED_LOCATION_COLLECTION, record, visited.atproto_record_uri)
    except Exception as e:  # noqa: BLE001 - outbox boundary, see module docstring
        visited.atproto_sync_pending = True
        visited.atproto_sync_error = str(e)
        await db.commit()
        return

    visited.atproto_record_uri = uri
    visited.atproto_record_cid = cid
    visited.atproto_sync_pending = False
    visited.atproto_sync_error = None
    await db.commit()


async def sync_travel_plan(db: AsyncSession, user: User, plan: TravelPlan) -> None:
    if not _sync_is_active(user):
        return
    try:
        session = await get_valid_session(db, user.id)
        record = travel_plan_to_record(plan)
        uri, cid = await _write_record(db, session, TRAVEL_PLAN_COLLECTION, record, plan.atproto_record_uri)
    except Exception as e:  # noqa: BLE001 - outbox boundary, see module docstring
        plan.atproto_sync_pending = True
        plan.atproto_sync_error = str(e)
        await db.commit()
        return

    plan.atproto_record_uri = uri
    plan.atproto_record_cid = cid
    plan.atproto_sync_pending = False
    plan.atproto_sync_error = None
    await db.commit()


async def delete_remote_record(db: AsyncSession, user: User, collection: str, record_uri: str | None) -> None:
    """Delete a PDS record given its *already-known* URI - the caller's
    local row may already be gone by the time this runs (it's meant to be
    called from a background task after the local delete), so this can't
    look the URI up itself.

    Best-effort: a failure here just leaves an orphaned record on the PDS,
    which is a smaller problem than a dangling local reference, so it's
    swallowed rather than surfaced. There's no local row left to mark
    sync_pending on this path - revisit with a small dead-letter table if
    orphaned PDS records turn out to be a real problem in practice.
    """
    if not (record_uri and _sync_is_active(user)):
        return
    try:
        session = await get_valid_session(db, user.id)
        await delete_record(db, session, collection, rkey_from_uri(record_uri))
    except Exception:  # noqa: BLE001 - best-effort, see docstring
        pass


async def sync_all_pending_for_user(db: AsyncSession, user: User) -> dict[str, int]:
    """Retry every atproto_sync_pending=True row this user owns. Used by the
    manual "sync now" endpoint (POST /auth/atproto/sync-pending) and equally
    callable from a cron/worker once one exists - see the "Failure handling"
    discussion in AT_PROTOCOL_MIGRATION.md section 7."""
    counts = {"wishlist_locations": 0, "visited_locations": 0, "travel_plans": 0}
    if not _sync_is_active(user):
        return counts

    result = await db.execute(
        select(WishlistLocation).where(
            WishlistLocation.owner_id == user.id, WishlistLocation.atproto_sync_pending.is_(True)
        )
    )
    for location in result.scalars().all():
        await sync_wishlist_location(db, user, location)
        counts["wishlist_locations"] += 1

    result = await db.execute(
        select(VisitedLocation).where(
            VisitedLocation.owner_id == user.id, VisitedLocation.atproto_sync_pending.is_(True)
        )
    )
    for visited in result.scalars().all():
        await sync_visited_location(db, user, visited)
        counts["visited_locations"] += 1

    result = await db.execute(
        select(TravelPlan).where(TravelPlan.user_id == user.id, TravelPlan.atproto_sync_pending.is_(True))
    )
    for plan in result.scalars().all():
        await sync_travel_plan(db, user, plan)
        counts["travel_plans"] += 1

    return counts


# --- Background-task-safe wrappers -----------------------------------------
#
# FastAPI's BackgroundTasks run *after* the response has been sent, by which
# point the request's `db` session (from app.database.get_db, an
# `async with`-scoped session) has already been closed - see get_db in
# app/database.py. Router endpoints must schedule these wrappers (which open
# their own session and re-fetch by id) rather than the sync_* functions
# above directly with the request's session/ORM objects.


async def sync_wishlist_location_task(user_id: int, location_id: int) -> None:
    async with async_session() as db:
        user = await db.get(User, user_id)
        location = await db.get(WishlistLocation, location_id)
        if user and location:
            await sync_wishlist_location(db, user, location)


async def sync_visited_location_task(user_id: int, visited_id: int) -> None:
    async with async_session() as db:
        user = await db.get(User, user_id)
        visited = await db.get(VisitedLocation, visited_id)
        if user and visited:
            await sync_visited_location(db, user, visited)


async def sync_travel_plan_task(user_id: int, plan_id: int) -> None:
    async with async_session() as db:
        user = await db.get(User, user_id)
        plan = await db.get(TravelPlan, plan_id)
        if user and plan:
            await sync_travel_plan(db, user, plan)


async def delete_remote_record_task(user_id: int, collection: str, record_uri: str | None) -> None:
    if not record_uri:
        return
    async with async_session() as db:
        user = await db.get(User, user_id)
        if user:
            await delete_remote_record(db, user, collection, record_uri)
