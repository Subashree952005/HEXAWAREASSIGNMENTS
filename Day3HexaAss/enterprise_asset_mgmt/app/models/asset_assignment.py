from sqlalchemy import Column, Integer, ForeignKey, Date, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin


class AssetAssignment(Base, TimestampMixin):
    __tablename__ = "asset_assignments"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_date = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)
    condition_on_return = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    asset = relationship("Asset", back_populates="assignments")
    user = relationship("User", back_populates="assignments", foreign_keys=[user_id])
    assigner = relationship("User", foreign_keys=[assigned_by])