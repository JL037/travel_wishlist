from app.database import Base
from sqlalchemy import String, DateTime, func, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .location import WishlistLocation, VisitedLocation
    from app.models.user_saved_city import UserSavedCity
    from app.models.travel_plan import TravelPlan
    from app.models.refresh_tokens import RefreshToken
    from app.models.atproto_session import AtprotoSession


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Nullable because AT Protocol-only accounts aren't required to expose an
    # email to us - their identity is their DID.
    email: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    username: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # Nullable because AT Protocol-only accounts (see app/models/atproto_session.py)
    # have no local password - they authenticate entirely via their PDS.
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)

    # AT Protocol identity, once this account has been linked to one.
    did: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    pds_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # Phase 2 (dual-write) opt-in - per-user, since it requires an active
    # AT Proto identity and changes what happens on every write. Meaningless
    # (and never checked) unless `did` is also set.
    atproto_sync_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    locations: Mapped[list["WishlistLocation"]] = relationship(
        "WishlistLocation", back_populates="owner", cascade="all, delete-orphan"
    )

    visited_locations: Mapped[list["VisitedLocation"]] = relationship(
        "VisitedLocation", back_populates="owner", cascade="all, delete-orphan"
    )

    saved_cities: Mapped[list["UserSavedCity"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    travel_plans: Mapped[list["TravelPlan"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete")
    atproto_session: Mapped[Optional["AtprotoSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )