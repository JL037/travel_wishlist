from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schema.user import UserRead, UserCreate
from app.models.users import User
from app.database import get_db
from app.utils.security import create_access_token, hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from app.dependencies.auth import get_current_user
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user_data.password)

    new_user = User(
        email=user_data.email, hashed_password=hashed_pwd, role=user_data.role
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

    return new_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        user_id=user.id, expires_delta=access_token_expires  # or user.email
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
