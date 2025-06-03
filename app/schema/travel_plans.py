from pydantic import BaseModel
from datetime import date

class TravelPlanCreate(BaseModel):
    date: date
    location: str
    notes: str | None = None

class TravelPlanOut(BaseModel):
    id: int
    date: date
    location: str
    notes: str | None
    