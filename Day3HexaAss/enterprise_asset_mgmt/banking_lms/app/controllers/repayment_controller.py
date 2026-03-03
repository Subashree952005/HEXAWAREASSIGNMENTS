from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.repayment_schema import (
    RepaymentCreate,
    RepaymentResponse
)
from app.services.repayment_service import RepaymentService
print("REPAYMENT CONTROLLER LOADED")
router = APIRouter(prefix="/repayments", tags=["Repayments"])

@router.post("/", response_model=RepaymentResponse)
def create_repayment(data: RepaymentCreate, db: Session = Depends(get_db)):
    return RepaymentService.create_repayment(db, data)