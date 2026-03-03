from fastapi import APIRouter, HTTPException
from app.schemas.course_schema import CourseCreate, CourseResponse
from app.services import course_service

router = APIRouter()

@router.post("", response_model=CourseResponse, status_code=201)
def create_course(data: CourseCreate):
    course = course_service.create_course(data.title, data.duration)
    return course.__dict__

@router.get("", response_model=list[CourseResponse])
def list_courses():
    return [c.__dict__ for c in course_service.list_courses()]

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    try:
        return course_service.get_course(course_id).__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
