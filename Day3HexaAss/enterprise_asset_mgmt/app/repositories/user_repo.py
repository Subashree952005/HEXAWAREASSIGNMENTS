from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password


class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreate) -> User:
        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            department_id=data.department_id,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id, User.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email, User.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 20) -> tuple[List[User], int]:
        count_result = await self.db.execute(
            select(func.count()).select_from(User).where(User.is_deleted == False)
        )
        total = count_result.scalar()
        result = await self.db.execute(
            select(User).where(User.is_deleted == False).offset(offset).limit(limit)
        )
        return result.scalars().all(), total

    async def get_by_department(self, dept_id: int) -> List[User]:
        result = await self.db.execute(
            select(User).where(User.department_id == dept_id, User.is_deleted == False)
        )
        return result.scalars().all()

    async def update(self, user: User, data: UserUpdate) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def soft_delete(self, user: User) -> User:
        user.is_deleted = True
        await self.db.flush()
        return user