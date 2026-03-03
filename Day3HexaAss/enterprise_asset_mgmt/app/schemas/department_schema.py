from typing import Optional
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentOut(BaseModel):
    id: int
    name: str
    manager_id: Optional[int]

    class Config:
        from_attributes = True