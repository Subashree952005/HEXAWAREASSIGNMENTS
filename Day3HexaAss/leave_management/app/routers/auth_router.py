from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user_schema import UserCreate, LoginRequest, TokenResponse, UserResponse
from app.controllers.auth_controller import register, login

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register_route(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return register(data, db)

@router.post("/login", response_model=TokenResponse)
def login_route(data: LoginRequest, db: Session = Depends(get_db)):
    """Login and receive JWT token"""
    return login(data, db)