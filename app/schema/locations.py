from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from app.schema.validators import (
    strip_and_validate_not_empty,
    validate_country_format,
    validate_latitude,
    validate_longitude,
)


class WishlistLocationBase(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] | None = None
    visited: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    proposed_date: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        return v.strip()

    @field_validator("city")
    @classmethod
    def validate_city(cls, v: str | None) -> str | None:
        return strip_and_validate_not_empty(v)

    @field_validator("country")
    @classmethod
    def validate_country(cls, v: str | None) -> str | None:
        return validate_country_format(v)

    @field_validator("latitude")
    @classmethod
    def validate_lat(cls, v: float | None) -> float | None:
        if v is None:
            return None
        return validate_latitude(v)

    @field_validator("longitude")
    @classmethod
    def validate_lon(cls, v: float | None) -> float | None:
        if v is None:
            return None
        return validate_longitude(v)


class WishlistLocationCreate(WishlistLocationBase):
    name: Optional[str] = None
    city: str
    country: str
    description: Optional[str] = None
    visited: bool = False
    notes: Optional[str] = None
    proposed_date: Optional[datetime] = None



class WishlistLocationUpdate(WishlistLocationBase):
    name: str | None = None
    description: Optional[str] = None
    visited: bool | None = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    proposed_date: Optional[datetime] = None
    visited: Optional[bool] = None


class WishlistLocationOut(WishlistLocationBase):
    id: int
    added_on: datetime
    city: str
    country: str
    notes: Optional[str] = None
    proposed_date: Optional[datetime] = None
    visited: bool

    model_config = ConfigDict(from_attributes=True)


class VisitedLocationBase(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[int] = None
    notes: Optional[str] = None
    visited_on: Optional[datetime] = None


class VisitedItemCreate(VisitedLocationBase):
    wishlist_id: int


class VisitedItemUpdate(VisitedLocationBase):
    notes: Optional[str] = None
    visited_on: Optional[datetime] = None
    rating: Optional[int] = None


class VisitedWithDetailsOut(BaseModel):
    id: int
    wishlist_id: int
    name: Optional[str] = None
    city: str
    country: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    visited_on: datetime
    rating: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
