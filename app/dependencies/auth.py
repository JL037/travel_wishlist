from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from app.core.config import settings
from app.database import get_db
from app.models.users import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="BearerAuth")


def get_token_from_request(request: Request):
    # 🍪 Always rely on the access_token in cookies (no headers anymore!)
    cookie_token = request.cookies.get("access_token")
    print("🍪 Cookie token received:", cookie_token)
    return cookie_token


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> User:
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

    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user
