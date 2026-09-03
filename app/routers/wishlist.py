from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app import crud
from app.database import get_db
from app.schema import locations
from app.dependencies.auth import get_current_user
from app.models.location import VisitedLocation, WishlistLocation
from app.models.users import User
from app.services.wishlist_services import create_location
from app.services.atproto_sync import (
    delete_remote_record_task,
    sync_visited_location_task,
    sync_wishlist_location_task,
)
from app.utils.atproto_lexicons import WISHLIST_LOCATION_COLLECTION

router = APIRouter(prefix="/wishlist", tags=["Wishlist Items"])


@router.post("", response_model=locations.WishlistLocationOut)
async def create_wishlist_item(
    item: locations.WishlistLocationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_location = await create_location(item, current_user.id, db)
    background_tasks.add_task(sync_wishlist_location_task, current_user.id, new_location.id)

    if item.visited:
        result = await db.execute(
            select(VisitedLocation).where(VisitedLocation.wishlist_id == new_location.id)
        )
        new_visited = result.scalar_one_or_none()
        if new_visited:
            background_tasks.add_task(sync_visited_location_task, current_user.id, new_visited.id)

    return new_location


@router.get("", response_model=list[locations.WishlistLocationOut])
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
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    #  Call the service function directly!
    updated_location = await crud.update_wishlist_location(
        db=db, location_id=wishlist_id, updates=location_data, user_id=current_user.id
    )

    if not updated_location:
        raise HTTPException(status_code=404, detail="Location not found")

    background_tasks.add_task(sync_wishlist_location_task, current_user.id, updated_location.id)

    # update_wishlist_location() also creates a VisitedLocation the first
    # time `visited` flips to True - sync it too if that just happened.
    if updated_location.visited:
        result = await db.execute(
            select(VisitedLocation).where(VisitedLocation.wishlist_id == updated_location.id)
        )
        visited = result.scalar_one_or_none()
        if visited:
            background_tasks.add_task(sync_visited_location_task, current_user.id, visited.id)

    return updated_location


@router.delete("/{wishlist_id}", status_code=204)
async def delete_location(
    wishlist_id: int,
    background_tasks: BackgroundTasks,
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

    record_uri = location.atproto_record_uri
    await db.delete(location)
    await db.commit()

    background_tasks.add_task(
        delete_remote_record_task, current_user.id, WISHLIST_LOCATION_COLLECTION, record_uri
    )
    return Response(status_code=204)
