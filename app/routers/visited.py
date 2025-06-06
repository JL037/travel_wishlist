from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.location import VisitedLocation, WishlistLocation
from app.schema.locations import VisitedWithDetailsOut
from app.dependencies.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/visited", tags=["Visited Locations"])


@router.get("", response_model=list[VisitedWithDetailsOut], status_code=status.HTTP_200_OK)
async def get_visited_with_details(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
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


@router.delete("/{visited_location_id}", status_code=status.HTTP_200_OK)
async def delete_visited_location(
    visited_location_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(VisitedLocation).where(
        VisitedLocation.id == visited_location_id,
        VisitedLocation.owner_id == current_user.id
    )
    result = await db.execute(stmt)
    visited_location = result.scalar_one_or_none()

    if not visited_location:
        raise HTTPException(
            status_code=404,
            detail="Visited location not found or not authorized to delete"
        )

    await db.delete(visited_location)
    await db.commit()

    return {"message": "Visited location deleted."}
