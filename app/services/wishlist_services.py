from sqlalchemy.orm import Session
from app.models.location import WishlistLocation


def get_all_items(db: Session):
    return db.query(WishlistLocation).order_by(WishlistLocation.added_on.desc()).all()
