from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.location import WishlistLocation, VisitedLocation
from app.utils.geocoding import get_lat_lon
from app.schema.locations import WishlistLocationCreate
from fastapi import HTTPException
from datetime import datetime, timezone


def get_all_items(db: Session):
    return db.query(WishlistLocation).order_by(WishlistLocation.added_on.desc()).all()


async def create_location(
    item: WishlistLocationCreate, user_id: int, db: AsyncSession
) -> WishlistLocation:
    latlon = await get_lat_lon(item.city, item.country)

    if latlon is None:
        raise HTTPException(
            status_code=400,
            detail=f"Could not find coordinates for '{item.city}'"
            + (f", '{item.country}'" if item.country else ""),
        )

    new_data = item.model_dump(exclude_unset=True)
    new_data["owner_id"] = user_id
    new_data["latitude"] = latlon[0]
    new_data["longitude"] = latlon[1]

    new_location = WishlistLocation(**new_data)
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)

    if item.visited:
        visited = VisitedLocation(
            wishlist_id=new_location.id,
            owner_id=user_id,
            visited_on=datetime.now(timezone.utc),
        )
        db.add(visited)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            print("❌ DB error while inserting VisitedLocation:", e)
            raise

    return new_location
