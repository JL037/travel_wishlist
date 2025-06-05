from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.travel_plan import TravelPlan
from app.models.users import User
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schema.travel_plans import TravelPlanCreate, TravelPlanOut

router = APIRouter(tags=["Travel Plans"])


@router.post("/travel-plans", response_model=TravelPlanOut, status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan: TravelPlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_plan = TravelPlan(user_id=current_user.id, **plan.model_dump())
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan


@router.get("/travel-plans", response_model=list[TravelPlanOut], status_code=status.HTTP_200_OK)
async def get_plans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(TravelPlan).where(TravelPlan.user_id == current_user.id)
    )
    return result.scalars().all()


@router.delete("/travel-plans/{plan_id}", status_code=status.HTTP_200_OK)
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = await db.get(TravelPlan, plan_id)
    if not plan or plan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Travel plan not found or not authorized to delete")

    await db.delete(plan)
    await db.commit()
    return {"message": "Travel plan deleted successfully."}
