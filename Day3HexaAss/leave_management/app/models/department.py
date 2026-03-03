from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    manager = relationship("User", foreign_keys=[manager_id])