from typing import Optional
from sqlalchemy import ForeignKey, String, DateTime, func, Integer, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.users import User


class WishlistLocation(Base):
    __tablename__ = "wishlist_location"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    visited: Mapped[bool] = mapped_column(default=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    added_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="locations")
    visited_locations: Mapped[list["VisitedLocation"]] = relationship(
        back_populates="wishlist_location"
    )


class VisitedLocation(Base):
    __tablename__ = "visited_location"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    wishlist_id: Mapped[int] = mapped_column(
        ForeignKey("wishlist_location.id"), nullable=False
    )
    visited_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


    owner: Mapped["User"] = relationship(back_populates="visited_locations")

    wishlist_location: Mapped["WishlistLocation"] = relationship(
        back_populates="visited_locations"
    )
