from sqlalchemy.orm import Session
from app.models.user import User

class UserService:

    @staticmethod
    def create_user(db: Session, data):
        user = User(
            name=data.name,
            email=data.email,
            role=data.role,
            password=data.password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()