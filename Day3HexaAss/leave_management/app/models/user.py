from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.EMPLOYEE, nullable=False)
    department_id = Column(Integer, nullable=True)

    leave_requests = relationship("LeaveRequest", back_populates="employee", foreign_keys="LeaveRequest.employee_id")