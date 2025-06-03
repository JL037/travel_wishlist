from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.user import UserRead, UserCreate, LoginData
from app.models.users import User
from app.database import get_db
from app.utils.security import create_access_token, hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from app.dependencies.auth import get_current_user
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email, username=user_data.username, hashed_password=hashed_pwd, role=user_data.role
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

    return new_user


@router.post("/login")
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        user_id=user.id, expires_delta=access_token_expires
    )

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
    )

    return response


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# @router.get("/test-auth")
# def test_auth(
#     token: str = Security(oauth2_scheme), current_user: User = Depends(get_current_user)
# ):
#     print("🔥🔥🔥 THIS IS DEFINITELY RUNNING 🔥🔥🔥")
#     print("🐢 Token received manually:", token)
#     return {"token": token}


@router.post("/auth/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    print("🔴 Access token cookie deleted")
    return response


@router.get("/api/test")
async def test_endpoint():
    return {"message": "Hello from backend!"}
