from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repo import UserRepo
from app.repositories.department_repo import DepartmentRepo
from app.schemas.user_schema import UserCreate, UserUpdate
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from app.core.pagination import PaginationParams, PaginatedResponse


class SuperAdminController:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepo(db)
        self.dept_repo = DepartmentRepo(db)

    # ── Users ──────────────────────────────────────────────
    async def create_user(self, data: UserCreate):
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        return await self.user_repo.create(data)

    async def list_users(self, params: PaginationParams):
        items, total = await self.user_repo.get_all(offset=params.offset, limit=params.size)
        return PaginatedResponse.create(items, total, params)

    async def get_user(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(self, user_id: int, data: UserUpdate):
        user = await self.get_user(user_id)
        return await self.user_repo.update(user, data)

    async def delete_user(self, user_id: int):
        user = await self.get_user(user_id)
        return await self.user_repo.soft_delete(user)

    # ── Departments ────────────────────────────────────────
    async def create_department(self, data: DepartmentCreate):
        return await self.dept_repo.create(data)

    async def list_departments(self, params: PaginationParams):
        items, total = await self.dept_repo.get_all(offset=params.offset, limit=params.size)
        return PaginatedResponse.create(items, total, params)

    async def get_department(self, dept_id: int):
        dept = await self.dept_repo.get_by_id(dept_id)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
        return dept

    async def update_department(self, dept_id: int, data: DepartmentUpdate):
        dept = await self.get_department(dept_id)
        return await self.dept_repo.update(dept, data)

    async def delete_department(self, dept_id: int):
        dept = await self.get_department(dept_id)
        return await self.dept_repo.soft_delete(dept)