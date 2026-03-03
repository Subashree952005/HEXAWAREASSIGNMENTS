from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class LoanProduct(Base):
    __tablename__ = "loan_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    max_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)

    applications = relationship("LoanApplication", back_populates="product")