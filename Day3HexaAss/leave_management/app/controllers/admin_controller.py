from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from app.schemas.leave_schema import LeaveStatusUpdate
from app.services.user_service import user_service
from app.services.department_service import dept_service
from app.services.leave_service import leave_service
from app.core.pagination import PaginationParams, PaginatedResponse
from app.models.user import User

# ─── Users ────────────────────────────────────────────────────────────────────

def create_user(data: UserCreate, db: Session):
    return user_service.create_user(db, data)

def list_users(pg: PaginationParams, db: Session):
    total, items = user_service.get_all_users(db, pg.offset, pg.limit)
    return PaginatedResponse(total=total, page=pg.page, size=pg.size, items=items)

def get_user(user_id: int, db: Session):
    return user_service.get_user(db, user_id)

def update_user(user_id: int, data: UserUpdate, db: Session):
    return user_service.update_user(db, user_id, data)

def delete_user(user_id: int, db: Session):
    return user_service.delete_user(db, user_id)

# ─── Departments ──────────────────────────────────────────────────────────────

def create_dept(data: DepartmentCreate, db: Session):
    return dept_service.create_department(db, data)

def list_depts(pg: PaginationParams, db: Session):
    total, items = dept_service.get_all(db, pg.offset, pg.limit)
    return PaginatedResponse(total=total, page=pg.page, size=pg.size, items=items)

def update_dept(dept_id: int, data: DepartmentUpdate, db: Session):
    return dept_service.update_department(db, dept_id, data)

def delete_dept(dept_id: int, db: Session):
    return dept_service.delete_department(db, dept_id)

# ─── Leaves ───────────────────────────────────────────────────────────────────

def list_all_leaves(pg: PaginationParams, db: Session):
    total, items = leave_service.get_all_leaves(db, pg.offset, pg.limit)
    return PaginatedResponse(total=total, page=pg.page, size=pg.size, items=items)

def override_leave(leave_id: int, data: LeaveStatusUpdate, admin: User, db: Session):
    return leave_service.admin_override(db, leave_id, data, admin)

def delete_leave(leave_id: int, db: Session):
    return leave_service.delete_leave(db, leave_id)