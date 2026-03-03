from fastapi import APIRouter, HTTPException
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse
from app.services import enrollment_service

router = APIRouter()

@router.post("", response_model=EnrollmentResponse, status_code=201)
def enroll_student(data: EnrollmentCreate):
    try:
        enrollment = enrollment_service.enroll_student(
            data.student_id, data.course_id
        )
        return enrollment.__dict__
    except ValueError as e:
        if "Already" in str(e):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))

@router.get("", response_model=list[EnrollmentResponse])
def get_all_enrollments():
    return [e.__dict__ for e in enrollment_service.get_all_enrollments()]

@router.get("/student/{student_id}")
def get_by_student(student_id: int):
    return [
        {"course_id": e.course_id}
        for e in enrollment_service.get_enrollments_by_student(student_id)
    ]

@router.get("/course/{course_id}")
def get_by_course(course_id: int):
    return [
        {"student_id": e.student_id}
        for e in enrollment_service.get_enrollments_by_course(course_id)
    ]
