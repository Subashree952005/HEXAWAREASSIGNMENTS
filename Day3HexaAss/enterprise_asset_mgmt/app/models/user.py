import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    IT_ADMIN = "IT_ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    department = relationship("Department", back_populates="users", foreign_keys="[User.department_id]")
    assignments = relationship("AssetAssignment", back_populates="user", foreign_keys="[AssetAssignment.user_id]")
    requests = relationship("AssetRequest", back_populates="employee", foreign_keys="[AssetRequest.employee_id]")
    approved_requests = relationship("AssetRequest", back_populates="approver", foreign_keys="[AssetRequest.approved_by]")
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys="[AuditLog.user_id]")