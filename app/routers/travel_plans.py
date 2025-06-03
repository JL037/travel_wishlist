from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.travel_plan import TravelPlan
from app.models.users import User
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schema.travel_plans import TravelPlanCreate, TravelPlanOut
from sqlalchemy import select


router = APIRouter()

@router.post("/travel-plans", response_model=TravelPlanOut)
async def create_plan(plan: TravelPlanCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_plan = TravelPlan(user_id=current_user.id, **plan.model_dump())
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan

@router.get("/travel-plans", response_model=list[TravelPlanOut])
async def get_plans(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(TravelPlan).where(TravelPlan.user_id == current_user.id))
    return result.scalars().all()