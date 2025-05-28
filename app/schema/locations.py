from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WishlistLocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    visited: bool = False


class WishlistLocationCreate(WishlistLocationBase):
    pass


class WishlistLocationUpdate(BaseModel):
    name: str | None = None
    description: Optional[str] = None
    visited: bool | None = None


class WishlistLocationOut(WishlistLocationBase):
    id: int
    added_on: datetime

    class Config:
        from_attributes = True


class VisitedLocationBase(BaseModel):
    rating: Optional[int] = None
    notes: Optional[str] = None
    visited_on: Optional[datetime] = None


class VisitedItemCreate(VisitedLocationBase):
    wishlist_id: int


class VisitedItemUpdate(VisitedLocationBase):
    pass


class VisitedItemOut(VisitedLocationBase):
    id: int
    wishlist_id: int

    class Config:
        from_attributes = True
