from fastapi import APIRouter, HTTPException
from app.schemas.student_schema import StudentCreate, StudentResponse
from app.services import student_service

router = APIRouter()

@router.post("", response_model=StudentResponse, status_code=201)
def register_student(data: StudentCreate):
    student = student_service.register_student(data.name, data.email)
    return student.__dict__

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    try:
        student = student_service.get_student(student_id)
        return student.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
