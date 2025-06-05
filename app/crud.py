from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from datetime import timezone, datetime
from app.models.location import WishlistLocation, VisitedLocation
from app.schema.locations import WishlistLocationCreate, WishlistLocationUpdate
from app.models.refresh_tokens import RefreshToken


async def create_wishlist_location(
    db: AsyncSession, location_data: WishlistLocationCreate, user_id: int
) -> WishlistLocation:
    new_location = WishlistLocation(
        name=location_data.name,
        city=location_data.city,
        country=location_data.country,
        description=location_data.description,
        visited=location_data.visited,
        owner_id=user_id,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)

    # ✅ If marked as visited, create VisitedLocation entry
    if location_data.visited:
        print("🟩 Creating VisitedLocation with:")
        print(" - wishlist_id:", new_location.id)
        print(" - owner_id:", user_id)

        visited = VisitedLocation(
            wishlist_id=new_location.id,
            owner_id=user_id,
            visited_on=datetime.now(timezone.utc),
            latitude=location_data.latitude,
            longitude=location_data.longitude,
        )
        db.add(visited)
        try:
            await db.commit()
            await db.refresh(visited)
        except SQLAlchemyError as e:
            await db.rollback()
            print("🔥 DB error while inserting VisitedLocation:", e)
            raise

    return new_location


async def get_wishlist_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(WishlistLocation).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_wishlist_location(
    db: AsyncSession, location_id: int, updates: WishlistLocationUpdate, user_id: int
):
    stmt = select(WishlistLocation).where(
        WishlistLocation.id == location_id, WishlistLocation.owner_id == user_id
    )
    result = await db.execute(stmt)
    location = result.scalar_one_or_none()

    if not location:
        return None

    original_visited = location.visited

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(location, field, value)

    await db.commit()
    await db.refresh(location)

    # ✅ If "visited" switched to True, ensure VisitedLocation exists
    if not original_visited and location.visited:
        stmt_visited = select(VisitedLocation).where(VisitedLocation.wishlist_id == location.id)
        result_visited = await db.execute(stmt_visited)
        already_visited = result_visited.scalar_one_or_none()

        if not already_visited:
            visited = VisitedLocation(
                wishlist_id=location.id,
                owner_id=user_id,
                visited_on=datetime.now(timezone.utc),
                latitude=location.latitude,
                longitude=location.longitude,
            )
            db.add(visited)
            await db.commit()
            await db.refresh(visited)

        print("UPDATE: location_id:", location_id)
        print("UPDATE: updates:", updates.model_dump(exclude_unset=True))
        print("UPDATE: found location:", location)

    return location


async def delete_wishlist_item(db: AsyncSession, item_id: int):
    stmt = select(WishlistLocation).where(WishlistLocation.id == item_id)
    result = await db.execute(stmt)
    db_item = result.scalar_one_or_none()
    if db_item:
        await db.delete(db_item)
        await db.commit()
    return db_item


async def store_refresh_token(db: AsyncSession, user_id: int, token: str):
    new_token = RefreshToken(
        user_id=user_id,
        token=token,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)
    return new_token


async def delete_refresh_token(db: AsyncSession, token: str):
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    db_token = result.scalar_one_or_none()
    if db_token:
        await db.delete(db_token)
        await db.commit()


async def get_refresh_token(db: AsyncSession, token: str):
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    return result.scalar_one_or_none()
