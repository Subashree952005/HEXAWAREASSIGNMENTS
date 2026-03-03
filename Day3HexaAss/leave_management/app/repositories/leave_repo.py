from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.leave_request import LeaveRequest, LeaveStatus
from app.schemas.leave_schema import LeaveCreate
from datetime import date

class LeaveRepository:
    def get_by_id(self, db: Session, leave_id: int):
        return db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    def get_all(self, db: Session, offset: int = 0, limit: int = 10):
        total = db.query(LeaveRequest).count()
        items = db.query(LeaveRequest).offset(offset).limit(limit).all()
        return total, items

    def get_by_employee(self, db: Session, employee_id: int):
        return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()

    def get_by_department(self, db: Session, employee_ids: list, offset: int = 0, limit: int = 10):
        total = db.query(LeaveRequest).filter(LeaveRequest.employee_id.in_(employee_ids)).count()
        items = db.query(LeaveRequest).filter(LeaveRequest.employee_id.in_(employee_ids)).offset(offset).limit(limit).all()
        return total, items

    def check_overlap(self, db: Session, employee_id: int, start: date, end: date):
        return db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status != LeaveStatus.REJECTED,
            and_(LeaveRequest.start_date <= end, LeaveRequest.end_date >= start)
        ).first()

    def create(self, db: Session, employee_id: int, data: LeaveCreate):
        leave = LeaveRequest(
            employee_id=employee_id,
            start_date=data.start_date,
            end_date=data.end_date,
            reason=data.reason,
            status=LeaveStatus.PENDING
        )
        db.add(leave)
        db.commit()
        db.refresh(leave)
        return leave

    def update_status(self, db: Session, leave: LeaveRequest, status: LeaveStatus, approver_id: int):
        leave.status = status
        leave.approved_by = approver_id
        db.commit()
        db.refresh(leave)
        return leave

    def delete(self, db: Session, leave: LeaveRequest):
        db.delete(leave)
        db.commit()

leave_repo = LeaveRepository()