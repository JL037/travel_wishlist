from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from app.models.users import UserRole
from app.schema.validators import validate_username


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

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    
    @field_validator("username")
    @classmethod
    def validate_username_field(cls, value):
        if value is not None:
            return validate_username(value)
        return value
    
class LoginData(BaseModel):
    email: str
    password: str


class UserInDB(UserRead):
    hashed_password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    