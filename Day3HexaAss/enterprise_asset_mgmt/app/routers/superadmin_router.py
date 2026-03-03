from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.rbac import require_superadmin
from app.repositories.user_repo import UserRepo
from app.repositories.department_repo import DepartmentRepo
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentOut
from app.core.pagination import PaginationParams, PaginatedResponse

router = APIRouter(prefix="/superadmin", tags=["SuperAdmin"], dependencies=[Depends(require_superadmin)])


# ─── User Management ───────────────────────────────────────────────────────────

@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepo(db)
    return await repo.create(data)


@router.get("/users", response_model=PaginatedResponse[UserOut])
async def list_users(params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    repo = UserRepo(db)
    items, total = await repo.get_all(offset=params.offset, limit=params.size)
    return PaginatedResponse.create(items, total, params)


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    repo = UserRepo(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    repo = UserRepo(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update(user, data)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    repo = UserRepo(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await repo.soft_delete(user)


# ─── Department Management ─────────────────────────────────────────────────────

@router.post("/departments", response_model=DepartmentOut, status_code=201)
async def create_department(data: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    repo = DepartmentRepo(db)
    return await repo.create(data)


@router.get("/departments", response_model=PaginatedResponse[DepartmentOut])
async def list_departments(params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    repo = DepartmentRepo(db)
    items, total = await repo.get_all(offset=params.offset, limit=params.size)
    return PaginatedResponse.create(items, total, params)


@router.patch("/departments/{dept_id}", response_model=DepartmentOut)
async def update_department(dept_id: int, data: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    repo = DepartmentRepo(db)
    dept = await repo.get_by_id(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return await repo.update(dept, data)


@router.delete("/departments/{dept_id}", status_code=204)
async def delete_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    repo = DepartmentRepo(db)
    dept = await repo.get_by_id(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    await repo.soft_delete(dept)