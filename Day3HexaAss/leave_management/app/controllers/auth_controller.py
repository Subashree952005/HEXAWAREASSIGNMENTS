from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, LoginRequest
from app.services.auth_service import auth_service

def register(data: UserCreate, db: Session):
    """Handle user registration"""
    return auth_service.register(db, data)

def login(data: LoginRequest, db: Session):
    """Handle user login and return token"""
    return auth_service.login(db, data)