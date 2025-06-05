from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.models.user_saved_city import UserSavedCity
from app.dependencies.auth import get_current_user
from app.schema.user_saved_city import CityOut, CityCreate

router = APIRouter(tags=["Saved Cities"])


@router.post("/user/saved-cities", response_model=CityOut, status_code=status.HTTP_201_CREATED)
async def save_city(
    city: CityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_city = UserSavedCity(user_id=current_user.id, city=city.city)
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return {"id": new_city.id, "city": new_city.city}


@router.get("/user/saved-cities", response_model=list[CityOut], status_code=status.HTTP_200_OK)
async def get_saved_cities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(UserSavedCity).where(UserSavedCity.user_id == current_user.id)
    )
    saved_cities = result.scalars().all()
    return [{"id": c.id, "city": c.city} for c in saved_cities]


@router.delete("/user/saved-cities/{city_id}", status_code=status.HTTP_200_OK)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    city = await db.get(UserSavedCity, city_id)
    if not city or city.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
    return {"message": "City deleted."}
