from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.users import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.USER


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    role: UserRole

    class Config:
        from_attributes = True


class UserInDB(UserRead):
    hashed_password: str
