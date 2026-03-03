from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.dependencies.rbac import require_manager
from app.schemas.leave_schema import LeaveResponse, LeaveStatusUpdate
from app.schemas.user_schema import UserResponse
from app.core.pagination import PaginationParams, PaginatedResponse
from app.controllers.manager_controller import get_dept_employees, get_dept_leaves, action_leave

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.get("/department/employees", response_model=List[UserResponse])
def get_dept_employees_route(db: Session = Depends(get_db), manager=Depends(require_manager)):
    """View all employees in manager's department"""
    return get_dept_employees(manager, db)

@router.get("/department/leaves", response_model=PaginatedResponse[LeaveResponse])
def get_dept_leaves_route(pg: PaginationParams = Depends(), db: Session = Depends(get_db), manager=Depends(require_manager)):
    """View all leave requests in manager's department"""
    return get_dept_leaves(pg, manager, db)

@router.patch("/leaves/{leave_id}/status", response_model=LeaveResponse)
def action_leave_route(leave_id: int, data: LeaveStatusUpdate, db: Session = Depends(get_db), manager=Depends(require_manager)):
    """Approve or Reject a leave request"""
    return action_leave(leave_id, data, manager, db)