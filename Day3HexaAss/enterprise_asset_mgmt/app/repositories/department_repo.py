from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.department import Department
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate


class DepartmentRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: DepartmentCreate) -> Department:
        dept = Department(**data.model_dump())
        self.db.add(dept)
        await self.db.flush()
        await self.db.refresh(dept)
        return dept

    async def get_by_id(self, dept_id: int) -> Optional[Department]:
        result = await self.db.execute(
            select(Department).where(Department.id == dept_id, Department.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 20) -> tuple[List[Department], int]:
        count = await self.db.execute(
            select(func.count()).select_from(Department).where(Department.is_deleted == False)
        )
        result = await self.db.execute(
            select(Department).where(Department.is_deleted == False).offset(offset).limit(limit)
        )
        return result.scalars().all(), count.scalar()

    async def update(self, dept: Department, data: DepartmentUpdate) -> Department:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(dept, field, value)
        await self.db.flush()
        await self.db.refresh(dept)
        return dept

    async def soft_delete(self, dept: Department) -> Department:
        dept.is_deleted = True
        await self.db.flush()
        return dept