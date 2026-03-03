from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import require_admin
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.leave_schema import LeaveResponse, LeaveStatusUpdate
from app.core.pagination import PaginationParams, PaginatedResponse
from app.controllers.admin_controller import (
    create_user, list_users, get_user, update_user, delete_user,
    create_dept, list_depts, update_dept, delete_dept,
    list_all_leaves, override_leave, delete_leave
)

router = APIRouter(prefix="/admin", tags=["Admin"])

# ─── Users ────────────────────────────────────────────────────────────────────

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user_route(data: UserCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return create_user(data, db)

@router.get("/users", response_model=PaginatedResponse[UserResponse])
def list_users_route(pg: PaginationParams = Depends(), db: Session = Depends(get_db), admin=Depends(require_admin)):
    return list_users(pg, db)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return get_user(user_id, db)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, data: UserUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return update_user(user_id, data, db)

@router.delete("/users/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return delete_user(user_id, db)

# ─── Departments ──────────────────────────────────────────────────────────────

@router.post("/departments", response_model=DepartmentResponse, status_code=201)
def create_dept_route(data: DepartmentCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return create_dept(data, db)

@router.get("/departments", response_model=PaginatedResponse[DepartmentResponse])
def list_depts_route(pg: PaginationParams = Depends(), db: Session = Depends(get_db), admin=Depends(require_admin)):
    return list_depts(pg, db)

@router.put("/departments/{dept_id}", response_model=DepartmentResponse)
def update_dept_route(dept_id: int, data: DepartmentUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return update_dept(dept_id, data, db)

@router.delete("/departments/{dept_id}")
def delete_dept_route(dept_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return delete_dept(dept_id, db)

# ─── Leaves ───────────────────────────────────────────────────────────────────

@router.get("/leaves", response_model=PaginatedResponse[LeaveResponse])
def list_all_leaves_route(pg: PaginationParams = Depends(), db: Session = Depends(get_db), admin=Depends(require_admin)):
    return list_all_leaves(pg, db)

@router.patch("/leaves/{leave_id}/status", response_model=LeaveResponse)
def override_leave_route(leave_id: int, data: LeaveStatusUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return override_leave(leave_id, data, admin, db)

@router.delete("/leaves/{leave_id}")
def delete_leave_route(leave_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return delete_leave(leave_id, db)