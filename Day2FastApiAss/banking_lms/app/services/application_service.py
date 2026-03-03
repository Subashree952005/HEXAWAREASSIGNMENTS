from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.loan_application import LoanApplication
from app.models.loan_product import LoanProduct
from app.models.user import User

class ApplicationService:

    @staticmethod
    def create_application(db: Session, data):
        product = db.query(LoanProduct).filter(
            LoanProduct.id == data.product_id
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if data.requested_amount > product.max_amount:
            raise HTTPException(
                status_code=400,
                detail="Requested amount exceeds product limit"
            )

        application = LoanApplication(
            requested_amount=data.requested_amount,
            outstanding_balance=data.requested_amount,
            user_id=data.user_id,
            product_id=data.product_id
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return application

    @staticmethod
    def update_status(db: Session, application_id: int, status_update, current_user_id: int):

        user = db.query(User).filter(User.id == current_user_id).first()

        if user.role != "loan_officer":
            raise HTTPException(status_code=403, detail="Not authorized")

        application = db.query(LoanApplication).filter(
            LoanApplication.id == application_id
        ).first()

        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        application.status = status_update.status

        db.commit()
        db.refresh(application)

        return application