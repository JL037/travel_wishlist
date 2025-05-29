from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserRead):
    hashed_password: str
