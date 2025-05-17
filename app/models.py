from typing import Optional, List
from sqlalchemy import ForeignKey, String, DateTime, func, Boolean, Integer, text, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(120))
    added_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    visited: Mapped[bool] = mapped_column(Boolean, default=False)

    visited_item: Mapped[Optional["VisitedItem"]] = relationship(back_populates="wishlist_item", cascade="all, delete-orphan", uselist=False)


class VisitedItem(Base):
    __tablename__ = "visited_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlist_items.id"), nullable=False)
    visited_on: Mapped[DateTime] = mapped_column(DateTime)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    wishlist_item: Mapped[Optional["WishlistItem"]] = relationship(back_populates="visited_item")