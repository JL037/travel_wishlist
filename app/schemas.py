from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WishlistItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    visited: bool = False

class WishlistItemCreate(WishlistItemBase):
    pass

class WishlistItemUpdate(WishlistItemBase):
    pass

class WishlistItemOut(WishlistItemBase):
    id: int
    added_on: datetime

    class Config:
        orm_mode = True

class VisitedItemBase(BaseModel):
    rating: Optional[int] = None
    notes: Optional[str] = None
    visited_on: Optional[datetime] = None

class VisitedItemCreate(VisitedItemBase):
    wishlist_id: int


class VisitedItemUpdate(VisitedItemBase):
    pass

class VisitedItemOut(VisitedItemBase):
    id: int
    wishlist_id: int

    class Config:
        orm_mode = True


