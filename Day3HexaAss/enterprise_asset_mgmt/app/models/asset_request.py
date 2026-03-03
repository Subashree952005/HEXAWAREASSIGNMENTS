import enum
from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, String
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin
from app.models.asset import AssetType


class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AssetRequest(Base, TimestampMixin):
    __tablename__ = "asset_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    rejection_reason = Column(Text, nullable=True)

    employee = relationship("User", back_populates="requests", foreign_keys=[employee_id])
    approver = relationship("User", back_populates="approved_requests", foreign_keys=[approved_by])