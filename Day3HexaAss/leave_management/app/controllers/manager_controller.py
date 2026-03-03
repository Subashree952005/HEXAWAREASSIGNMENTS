from sqlalchemy.orm import Session
from app.schemas.leave_schema import LeaveStatusUpdate
from app.services.leave_service import leave_service
from app.repositories.user_repo import user_repo
from app.core.pagination import PaginationParams, PaginatedResponse
from app.models.user import User

def get_dept_employees(manager: User, db: Session):
    """Get all employees in manager's department"""
    return user_repo.get_by_department(db, manager.department_id)

def get_dept_leaves(pg: PaginationParams, manager: User, db: Session):
    """Get all leave requests in manager's department"""
    total, items = leave_service.get_department_leaves(db, manager, pg.offset, pg.limit)
    return PaginatedResponse(total=total, page=pg.page, size=pg.size, items=items)

def action_leave(leave_id: int, data: LeaveStatusUpdate, manager: User, db: Session):
    """Approve or Reject a leave request"""
    return leave_service.manager_action(db, leave_id, data, manager)