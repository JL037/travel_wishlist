from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.location import VisitedLocation, WishlistLocation
from app.schema.locations import VisitedWithDetailsOut
from app.dependencies.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/visited", tags=["visited"])


@router.get("/", response_model=list[VisitedWithDetailsOut])
def get_visited_with_details(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    results = (
        db.query(
            VisitedLocation.id,
            VisitedLocation.wishlist_id,
            WishlistLocation.name,
            WishlistLocation.city,
            WishlistLocation.country,
            WishlistLocation.description,
            WishlistLocation.latitude,
            WishlistLocation.longitude,
            VisitedLocation.visited_on,
            VisitedLocation.rating,
            VisitedLocation.notes,
        )
        .join(WishlistLocation, VisitedLocation.wishlist_id == WishlistLocation.id)
        .filter(VisitedLocation.owner_id == current_user.id)
        .all()
    )
    return results
