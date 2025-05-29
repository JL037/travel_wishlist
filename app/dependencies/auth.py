from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User, UserRole
from jose import JWTError, jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="BearerAuth")


def get_token_from_request(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        print("🟢 Found token in Authorization header:", token)
        return token

    cookie_token = request.cookies.get("access_token")
    print("🍪 Cookie token received:", cookie_token)
    return cookie_token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = get_token_from_request(request)
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        print("🚨 Raw token received:", token)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        print("Decoded payload:", payload)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin priveleges required"
        )
    return current_user
