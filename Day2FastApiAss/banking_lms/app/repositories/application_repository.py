from sqlalchemy.orm import Session
from app.models.loan_application import LoanApplication

class ApplicationRepository:

    @staticmethod
    def create(db: Session, application):
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def get_by_id(db: Session, application_id: int):
        return db.query(LoanApplication).filter(
            LoanApplication.id == application_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(LoanApplication).all()

    @staticmethod
    def update(db: Session, application):
        db.commit()
        db.refresh(application)
        return application