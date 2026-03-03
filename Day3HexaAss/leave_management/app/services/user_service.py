from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repo import user_repo
from app.schemas.user_schema import UserCreate, UserUpdate

class UserService:
    def get_user(self, db: Session, user_id: int):
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_all_users(self, db: Session, offset: int, limit: int):
        return user_repo.get_all(db, offset, limit)

    def create_user(self, db: Session, data: UserCreate):
        if user_repo.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        return user_repo.create(db, data)

    def update_user(self, db: Session, user_id: int, data: UserUpdate):
        user = self.get_user(db, user_id)
        return user_repo.update(db, user, data)

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user(db, user_id)
        user_repo.delete(db, user)
        return {"message": "User deleted"}

user_service = UserService()