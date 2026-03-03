from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.leave_schema import LeaveCreate
from app.services.leave_service import leave_service
from app.models.user import User

def apply_leave(data: LeaveCreate, employee: User, db: Session):
    """Apply for a leave"""
    return leave_service.apply_leave(db, employee, data)

def my_leaves(employee: User, db: Session):
    """Get all leave requests of current employee"""
    return leave_service.get_my_leaves(db, employee.id)

def get_leave(leave_id: int, employee: User, db: Session):
    """Get a specific leave request"""
    leave = leave_service.get_leave_by_id(db, leave_id)
    if leave.employee_id != employee.id:
        raise HTTPException(status_code=403, detail="Not your leave request")
    return leave