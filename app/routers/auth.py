from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schema.user import UserRead, UserCreate
from app.models.users import User, UserRole
from app.database import get_db
from app.utils.security import create_access_token, hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from app.dependencies.auth import get_current_user
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(get_current_user)]
)

