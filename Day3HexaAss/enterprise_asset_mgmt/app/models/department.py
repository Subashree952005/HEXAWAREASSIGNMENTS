from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base, TimestampMixin


class Department(Base, TimestampMixin):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    users = relationship('User', back_populates='department', foreign_keys='User.department_id')
    manager = relationship('User', foreign_keys=[manager_id])
    assets = relationship('Asset', back_populates='department')
