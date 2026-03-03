from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.loan_application import LoanApplication
from app.models.repayment import Repayment

class RepaymentService:

    @staticmethod
    def create_repayment(db: Session, data):

        application = db.query(LoanApplication).filter(
            LoanApplication.id == data.application_id
        ).first()

        if application.status != "approved":
            raise HTTPException(
                status_code=400,
                detail="Loan not approved"
            )

        if data.amount > application.outstanding_balance:
            raise HTTPException(
                status_code=400,
                detail="Repayment exceeds balance"
            )

        application.outstanding_balance -= data.amount

        if application.outstanding_balance == 0:
            application.status = "closed"

        repayment = Repayment(
            amount=data.amount,
            application_id=data.application_id
        )

        db.add(repayment)
        db.commit()
        db.refresh(repayment)

        return repayment