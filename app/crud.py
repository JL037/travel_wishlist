from sqlalchemy.orm import Session
from datetime import timezone, datetime
from app.models.location import WishlistLocation, VisitedLocation
from app.schema.locations import (
    WishlistLocationCreate,
    WishlistLocationUpdate,
)


def create_wishlist_location(
    db: Session, location_data: WishlistLocationCreate, user_id: int
):
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
    db.commit()
    db.refresh(new_location)

    # if visited=True, also add to visited_location
    if location_data.visited:
        visited = VisitedLocation(
            wishlist_id=new_location.id,
            owner_id=user_id,
            visited_on=datetime.now(timezone.utc),
        )
        db.add(visited)
        db.commit()

    return new_location


def get_wishlist_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(WishlistLocation).offset(skip).limit(limit).all()


def update_wishlist_location(
    db: Session, location_id: int, updates: WishlistLocationUpdate, user_id: int
):
    location = (
        db.query(WishlistLocation)
        .filter(
            WishlistLocation.id == location_id, WishlistLocation.owner_id == user_id
        )
        .first()
    )

    if not location:
        return None

    original_visited = location.visited

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(location, field, value)

    db.commit()
    db.refresh(location)

    # If visited switched to True and not already in visited_location table
    if not original_visited and location.visited:
        already_visited = (
            db.query(VisitedLocation).filter_by(wishlist_id=location.id).first()
        )

        if not already_visited:
            visited = VisitedLocation(
                wishlist_id=location.id,
                owner_id=user_id,
                visited_on=datetime.now(timezone.utc),
            )
            db.add(visited)
            db.commit()

    return location


def delete_wishlist_item(db: Session, item_id: int):
    db_item = db.query(WishlistLocation).filter(WishlistLocation.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
