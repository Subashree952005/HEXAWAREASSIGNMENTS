from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    requested_amount: float
    user_id: int
    product_id: int

class ApplicationStatusUpdate(BaseModel):
    status: str

class ApplicationResponse(BaseModel):
    id: int
    requested_amount: float
    status: str
    outstanding_balance: float
    user_id: int
    product_id: int

    class Config:
        from_attributes = True