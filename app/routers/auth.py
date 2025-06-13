from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Body
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from jose import jwt, JWTError

from app.schema.user import UserRead, UserCreate, LoginData, UserUpdate, ChangePasswordRequest, ResetPasswordRequest
from app.models.users import User
from app.database import get_db
from app.utils.security import (
    create_access_token, hash_password, verify_password, create_refresh_token, create_reset_token, verify_reset_token
)
from app.dependencies.auth import get_current_user
from app.core.config import settings
from app.crud import store_refresh_token, get_refresh_token, delete_refresh_token
from app.services.email import send_password_reset_email

router = APIRouter(prefix="/auth", tags=["Auth"])


# @limiter.limit("2/minute")
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pwd,
        role=user_data.role
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

    return new_user


# @limiter.limit("5/minute")
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    data: LoginData,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        user_id=user.id,
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        user_id=user.id,
        expires_delta=refresh_token_expires
    )

    await store_refresh_token(db, user_id=user.id, token=refresh_token)

    response = JSONResponse(content={"message": "Login successful"})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
        max_age=1800,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        max_age=7 * 24 * 60 * 60,
    )

    return response


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    db_token = await get_refresh_token(db, refresh_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Rotate refresh token for security
    await delete_refresh_token(db, refresh_token)
    new_refresh_token = create_refresh_token(
        user_id=int(user_id),
        expires_delta=timedelta(days=7)
    )
    await store_refresh_token(db, user_id=int(user_id), token=new_refresh_token)

    access_token_expires = timedelta(minutes=30)
    new_access_token = create_access_token(
        user_id=int(user_id),
        expires_delta=access_token_expires
    )

    response = JSONResponse(content={"message": "Token refreshed"})
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="none",
        secure=True,
        max_age=1800,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        max_age=7 * 24 * 60 * 60,
    )
    return response


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_current_user(request: Request, current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await delete_refresh_token(db, refresh_token)

    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.get("/api/test", status_code=status.HTTP_200_OK)
async def test_endpoint():
    return {"message": "Hello from backend!"}

@router.post("/change-password")
async def change_password(password_data: ChangePasswordRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    current_user.hashed_password = hash_password(password_data.new_password)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {"message": "Password updated successfully"}

@router.put ("/me", response_model=dict)
async def update_profile(update_data: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_data = update_data.model_dump(exclude_unset=True)

    if "username" in user_data:
        result = await db.execute(select(User).where(User.username == user_data["username"]))
        existing = result.scalar_one_or_none()
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Username already in use")
        
    if "email" in user_data:
        result = await db.execute(select(User).where(User.email == user_data["email"]))
        existing = result.scalar_one_or_none()
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already in use")

    for field, value in user_data.items():
        setattr(current_user, field, value)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {"message": "Profile updated successfully"}

@router.delete("/delete-account", response_class=JSONResponse)
async def delete_account(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await db.delete(current_user)
    await db.commit()
    return {"message": "Account deleted successfully"}

@router.post("/forgot-password")
async def forgot_password(background_tasks: BackgroundTasks, email: EmailStr = Body(...), db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = create_reset_token(email)

    await send_password_reset_email(background_tasks, to_email=email, reset_token=token)

    return {"reset_token": token}


@router.post("/reset-password")
async def reset_password(pwd_data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    email = verify_reset_token(pwd_data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = hash_password(pwd_data.new_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "Password reset successfully"}
