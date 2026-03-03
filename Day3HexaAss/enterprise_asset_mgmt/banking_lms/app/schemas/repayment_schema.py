from pydantic import BaseModel

class RepaymentCreate(BaseModel):
    amount: float
    application_id: int

class RepaymentResponse(BaseModel):
    id: int
    amount: float
    application_id: int

    class Config:
        from_attributes = True