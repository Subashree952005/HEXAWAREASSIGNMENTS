from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date
from app.models.leave_request import LeaveStatus

class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")
        return self

class LeaveStatusUpdate(BaseModel):
    status: LeaveStatus

class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: str
    status: LeaveStatus
    approved_by: Optional[int] = None

    model_config = {"from_attributes": True}