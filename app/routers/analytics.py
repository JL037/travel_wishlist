from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.analytics import get_user_analytics
from app.dependencies.auth import get_current_user
from app.models.users import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/me")
async def fetch_my_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_user_analytics(current_user.id, db)
