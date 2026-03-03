from pydantic import BaseModel
from typing import Optional

class DepartmentCreate(BaseModel):
    name: str
    manager_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentResponse(BaseModel):
    id: int
    name: str
    manager_id: Optional[int] = None

    model_config = {"from_attributes": True}