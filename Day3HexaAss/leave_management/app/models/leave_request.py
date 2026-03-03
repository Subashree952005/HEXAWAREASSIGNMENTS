from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum

class LeaveStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING, nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    employee = relationship("User", back_populates="leave_requests", foreign_keys=[employee_id])
    approver = relationship("User", foreign_keys=[approved_by])