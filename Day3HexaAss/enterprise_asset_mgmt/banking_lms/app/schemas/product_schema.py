from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    max_amount: float
    interest_rate: float

class ProductResponse(BaseModel):
    id: int
    name: str
    max_amount: float
    interest_rate: float

    class Config:
        from_attributes = True