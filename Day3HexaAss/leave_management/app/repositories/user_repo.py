from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password

class UserRepository:
    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_all(self, db: Session, offset: int = 0, limit: int = 10):
        total = db.query(User).count()
        items = db.query(User).offset(offset).limit(limit).all()
        return total, items

    def create(self, db: Session, data: UserCreate):
        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            department_id=data.department_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, data: UserUpdate):
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User):
        db.delete(user)
        db.commit()

    def get_by_department(self, db: Session, department_id: int):
        return db.query(User).filter(User.department_id == department_id).all()

user_repo = UserRepository()