from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app import crud
from app.database import get_db
from app.schema import locations
from app.dependencies.auth import get_current_user
from app.models.location import WishlistLocation
from app.models.users import User
from app.services.wishlist_services import create_location

router = APIRouter(prefix="/wishlist", tags=["Wishlist Items"])


@router.post("/", response_model=locations.WishlistLocationOut)
async def create_wishlist_item(
    item: locations.WishlistLocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_location(item, current_user.id, db)


@router.get("/", response_model=list[locations.WishlistLocationOut])
async def read_wishlist_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: Optional[str] = Query(default=None),
    skip: int = 0,
    limit: int = 10,
):
    stmt = (
        select(WishlistLocation)
        .where(WishlistLocation.owner_id == current_user.id, ~WishlistLocation.visited)
        .offset(skip)
        .limit(limit)
    )
    if search:
        stmt = stmt.where(WishlistLocation.name.ilike(f"%{search}%"))

    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{wishlist_id}", response_model=locations.WishlistLocationOut)
async def read_location_by_id(
    wishlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(WishlistLocation).where(
        WishlistLocation.id == wishlist_id,
        WishlistLocation.owner_id == current_user.id,
    )
    result = await db.execute(stmt)
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return location


@router.patch("/{wishlist_id}", response_model=locations.WishlistLocationOut)
async def update_location(
    wishlist_id: int,
    location_data: locations.WishlistLocationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    #  Call the service function directly!
    updated_location = await crud.update_wishlist_location(
        db=db, location_id=wishlist_id, updates=location_data, user_id=current_user.id
    )

    if not updated_location:
        raise HTTPException(status_code=404, detail="Location not found")

    return updated_location


@router.delete("/{wishlist_id}", status_code=204)
async def delete_location(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(WishlistLocation).where(
        WishlistLocation.id == wishlist_id,
        WishlistLocation.owner_id == current_user.id,
    )
    result = await db.execute(stmt)
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=404, detail="location not found")

    await db.delete(location)
    await db.commit()
    return Response(status_code=204)
