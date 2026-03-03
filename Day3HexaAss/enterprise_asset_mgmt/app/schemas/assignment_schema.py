from typing import Optional
from datetime import date
from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    asset_id: int
    user_id: int
    assigned_date: date
    notes: Optional[str] = None


class AssignmentReturn(BaseModel):
    returned_date: date
    condition_on_return: Optional[str] = None
    notes: Optional[str] = None


class AssignmentOut(BaseModel):
    id: int
    asset_id: int
    user_id: int
    assigned_by: int
    assigned_date: date
    returned_date: Optional[date]
    condition_on_return: Optional[str]
    is_active: bool
    notes: Optional[str]

    class Config:
        from_attributes = True