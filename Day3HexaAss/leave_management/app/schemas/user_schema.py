from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import RoleEnum

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.EMPLOYEE
    department_id: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    department_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    department_id: Optional[int] = None

    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"