from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repo import user_repo
from app.schemas.user_schema import UserCreate, LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token

class AuthService:
    def register(self, db: Session, data: UserCreate):
        existing = user_repo.get_by_email(db, data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = user_repo.create(db, data)
        return user

    def login(self, db: Session, data: LoginRequest) -> TokenResponse:
        user = user_repo.get_by_email(db, data.email)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return TokenResponse(access_token=token)

auth_service = AuthService()