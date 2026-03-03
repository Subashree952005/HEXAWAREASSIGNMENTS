from fastapi import APIRouter, HTTPException
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanStatusResponse
from app.services import loan_service

router = APIRouter()

@router.post("", response_model=LoanResponse, status_code=201)
def submit_loan(data: LoanCreate):
    try:
        loan = loan_service.submit_loan(
            data.applicant_name,
            data.income,
            data.loan_amount
        )
        return loan.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int):
    try:
        return loan_service.get_loan(loan_id).__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("", response_model=list[LoanResponse])
def list_loans():
    return [l.__dict__ for l in loan_service.get_all_loans()]

@router.put("/{loan_id}/approve", response_model=LoanStatusResponse)
def approve_loan(loan_id: int):
    try:
        loan = loan_service.approve_loan(loan_id)
        return {"message": "Loan approved successfully", "status": loan.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{loan_id}/reject", response_model=LoanStatusResponse)
def reject_loan(loan_id: int):
    try:
        loan = loan_service.reject_loan(loan_id)
        return {"message": "Loan rejected", "status": loan.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
