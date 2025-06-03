from pydantic import BaseModel, ConfigDict

class CityCreate(BaseModel):
    city: str

class CityOut(BaseModel):
    id: int
    city: str

    model_config = ConfigDict(from_attributes=True)

