from sqlalchemy.orm import Session
from app.models.loan_product import LoanProduct

class LoanProductRepository:

    @staticmethod
    def create(db: Session, product_data):
        product = LoanProduct(**product_data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all(db: Session):
        return db.query(LoanProduct).all()