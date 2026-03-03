from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Repayment(Base):
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)

    application_id = Column(Integer, ForeignKey("loan_applications.id"))

    application = relationship("LoanApplication", back_populates="repayments")