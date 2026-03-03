from pydantic import BaseModel

class LoanCreate(BaseModel):
    applicant_name: str
    income: float
    loan_amount: float

class LoanResponse(BaseModel):
    id: int
    applicant_name: str
    income: float
    loan_amount: float
    status: str

class LoanStatusResponse(BaseModel):
    message: str
    status: str
