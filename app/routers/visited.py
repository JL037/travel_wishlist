from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.location import VisitedLocation, WishlistLocation
from app.schema.locations import VisitedWithDetailsOut
from app.dependencies.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/visited", tags=["visited"])


@router.get("/", response_model=list[VisitedWithDetailsOut])
async def get_visited_with_details(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    stmt = (
        select(
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
        .where(VisitedLocation.owner_id == current_user.id)
    )

    result = await db.execute(stmt)
    return result.mappings().all()
