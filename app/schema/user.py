from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.users import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: Optional[UserRole] = UserRole.USER


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class LoginData(BaseModel):
    username: str
    password: str


class UserInDB(UserRead):
    hashed_password: str
