from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.dependencies.rbac import require_employee
from app.schemas.leave_schema import LeaveCreate, LeaveResponse
from app.controllers.employee_controller import apply_leave, my_leaves, get_leave

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("/leaves", response_model=LeaveResponse, status_code=201)
def apply_leave_route(data: LeaveCreate, db: Session = Depends(get_db), employee=Depends(require_employee)):
    """Apply for a leave"""
    return apply_leave(data, employee, db)

@router.get("/leaves", response_model=List[LeaveResponse])
def my_leaves_route(db: Session = Depends(get_db), employee=Depends(require_employee)):
    """View all my leave requests"""
    return my_leaves(employee, db)

@router.get("/leaves/{leave_id}", response_model=LeaveResponse)
def get_leave_route(leave_id: int, db: Session = Depends(get_db), employee=Depends(require_employee)):
    """View a specific leave request"""
    return get_leave(leave_id, employee, db)