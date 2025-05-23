from sqlalchemy.orm import Session
from app.models import WishlistItem

def get_all_items(db: Session):
    return db.query(WishlistItem).order_by(WishlistItem.added_on.desc()).all()

