from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    location: str
    description: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)