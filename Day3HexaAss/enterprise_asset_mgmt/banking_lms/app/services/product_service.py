from sqlalchemy.orm import Session
from app.models.loan_product import LoanProduct

class ProductService:

    @staticmethod
    def create_product(db: Session, data):
        product = LoanProduct(
            name=data.name,
            max_amount=data.max_amount,
            interest_rate=data.interest_rate
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all_products(db: Session):
        return db.query(LoanProduct).all()