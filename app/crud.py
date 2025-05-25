from sqlalchemy.orm import Session
from models.location import WishlistLocation, VisitedLocation
from schema.locations import WishlistLocationCreate, WishlistLocationOut, WishlistLocationUpdate, VisitedItemCreate, VisitedItemOut, VisitedItemUpdate


def create_wishlist_item(db: Session, item: WishlistLocationCreate):
    db_item = WishlistLocation(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_wishlist_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(WishlistLocation).offset(skip).limit(limit).all()

def get_wishlist_items(db: Session, item_id: int):
    return db.query(WishlistLocation).filter(WishlistLocation.id == item_id).first()

def update_wishlist_item(db: Session, item_id: int, item: WishlistLocationUpdate):
    db_item = db.query(WishlistLocation).filter(WishlistLocation.id == item_id).first()
    if db_item:
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_wishlist_item(db: Session, item_id: int):
    db_item = db.query(WishlistLocation).filter(WishlistLocation.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

