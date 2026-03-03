import enum
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum, Date
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin


class AuditAction(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ASSIGN = "ASSIGN"
    RETURN = "RETURN"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    LOGIN = "LOGIN"


class MaintenanceStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(Enum(AuditAction), nullable=False)
    entity = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)

    user = relationship("User", back_populates="audit_logs")


class MaintenanceRecord(Base, TimestampMixin):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    completed_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="SCHEDULED")
    description = Column(Text, nullable=True)
    cost = Column(String(20), nullable=True)

    asset = relationship("Asset", back_populates="maintenance_records")