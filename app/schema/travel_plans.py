from pydantic import BaseModel
from datetime import datetime

class TravelPlanCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    location: str
    notes: str | None = None

class TravelPlanOut(TravelPlanCreate):
    id: int
    
    