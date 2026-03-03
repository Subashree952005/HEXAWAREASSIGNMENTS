from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.leave_repo import leave_repo
from app.repositories.user_repo import user_repo
from app.schemas.leave_schema import LeaveCreate, LeaveStatusUpdate
from app.models.leave_request import LeaveStatus
from app.models.user import User

class LeaveService:
    def apply_leave(self, db: Session, employee: User, data: LeaveCreate):
        # Validate overlap
        overlap = leave_repo.check_overlap(db, employee.id, data.start_date, data.end_date)
        if overlap:
            raise HTTPException(status_code=400, detail="Overlapping leave request exists")
        return leave_repo.create(db, employee.id, data)

    def get_my_leaves(self, db: Session, employee_id: int):
        return leave_repo.get_by_employee(db, employee_id)

    def get_leave_by_id(self, db: Session, leave_id: int):
        leave = leave_repo.get_by_id(db, leave_id)
        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")
        return leave

    def manager_action(self, db: Session, leave_id: int, data: LeaveStatusUpdate, manager: User):
        leave = self.get_leave_by_id(db, leave_id)
        # Validate leave belongs to manager's department
        employee = user_repo.get_by_id(db, leave.employee_id)
        if employee.department_id != manager.department_id:
            raise HTTPException(status_code=403, detail="Leave does not belong to your department")
        if leave.status != LeaveStatus.PENDING:
            raise HTTPException(status_code=400, detail="Only PENDING leaves can be actioned")
        return leave_repo.update_status(db, leave, data.status, manager.id)

    def admin_override(self, db: Session, leave_id: int, data: LeaveStatusUpdate, admin: User):
        leave = self.get_leave_by_id(db, leave_id)
        return leave_repo.update_status(db, leave, data.status, admin.id)

    def get_all_leaves(self, db: Session, offset: int, limit: int):
        return leave_repo.get_all(db, offset, limit)

    def get_department_leaves(self, db: Session, manager: User, offset: int, limit: int):
        employees = user_repo.get_by_department(db, manager.department_id)
        employee_ids = [e.id for e in employees]
        return leave_repo.get_by_department(db, employee_ids, offset, limit)

    def delete_leave(self, db: Session, leave_id: int):
        leave = self.get_leave_by_id(db, leave_id)
        leave_repo.delete(db, leave)
        return {"message": "Leave deleted"}

leave_service = LeaveService()