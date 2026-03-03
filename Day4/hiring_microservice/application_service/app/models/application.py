from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)
    status = Column(String, default="Applied")