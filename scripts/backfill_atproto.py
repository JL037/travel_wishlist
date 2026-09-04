"""One-time backfill: push pre-existing local rows to the PDS for users who
have opted into Phase 2 dual-write (see AT_PROTOCOL_MIGRATION.md section 10,
"Phase 2 - Dual-write").

New/edited rows sync automatically from here on (app/routers/wishlist.py,
visited.py, travel_plans.py schedule a background sync on write). This
script is only for rows that existed *before* a user turned dual-write on,
which the normal write-path sync never touches since nothing writes to them
again on its own.

Usage:
    python -m scripts.backfill_atproto [--user-id ID]

Safe to re-run: it only processes rows where atproto_record_uri is still
NULL, so already-synced rows and rows synced by a previous partial run are
skipped.
"""

import argparse
import asyncio

from sqlalchemy import select

from app.database import async_session
from app.models.location import VisitedLocation, WishlistLocation
from app.models.travel_plan import TravelPlan
from app.models.users import User
from app.services.atproto_sync import sync_travel_plan, sync_visited_location, sync_wishlist_location


async def backfill_user(db, user: User) -> dict[str, int]:
    counts = {"wishlist_locations": 0, "visited_locations": 0, "travel_plans": 0, "errors": 0}

    result = await db.execute(
        select(WishlistLocation).where(
            WishlistLocation.owner_id == user.id, WishlistLocation.atproto_record_uri.is_(None)
        )
    )
    wishlist_locations = result.scalars().all()
    for location in wishlist_locations:
        await sync_wishlist_location(db, user, location)
        if location.atproto_record_uri:
            counts["wishlist_locations"] += 1
        else:
            counts["errors"] += 1

    result = await db.execute(
        select(VisitedLocation).where(
            VisitedLocation.owner_id == user.id, VisitedLocation.atproto_record_uri.is_(None)
        )
    )
    visited_locations = result.scalars().all()
    for visited in visited_locations:
        await sync_visited_location(db, user, visited)
        if visited.atproto_record_uri:
            counts["visited_locations"] += 1
        else:
            counts["errors"] += 1

    result = await db.execute(
        select(TravelPlan).where(TravelPlan.user_id == user.id, TravelPlan.atproto_record_uri.is_(None))
    )
    plans = result.scalars().all()
    for plan in plans:
        await sync_travel_plan(db, user, plan)
        if plan.atproto_record_uri:
            counts["travel_plans"] += 1
        else:
            counts["errors"] += 1

    return counts


async def main(user_id: int | None) -> None:
    async with async_session() as db:
        stmt = select(User).where(User.atproto_sync_enabled.is_(True), User.did.is_not(None))
        if user_id is not None:
            stmt = stmt.where(User.id == user_id)
        result = await db.execute(stmt)
        users = result.scalars().all()

        if not users:
            print("No opted-in AT Protocol users found - nothing to backfill.")
            return

        for user in users:
            counts = await backfill_user(db, user)
            print(
                f"user {user.id} ({user.username}): "
                f"{counts['wishlist_locations']} wishlist, "
                f"{counts['visited_locations']} visited, "
                f"{counts['travel_plans']} travel plans synced"
                + (f", {counts['errors']} errors (see atproto_sync_error columns)" if counts["errors"] else "")
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user-id", type=int, default=None, help="Backfill only this user (default: all opted-in users)")
    args = parser.parse_args()
    asyncio.run(main(args.user_id))
