from app.database import Base
from sqlalchemy import String, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .location import WishlistLocation, VisitedLocation


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    locations: Mapped[list["WishlistLocation"]] = relationship(
        "WishlistLocation", back_populates="owner"
    )

    visited_locations: Mapped[list["VisitedLocation"]] = relationship(
        "VisitedLocation", back_populates="owner"
    )
