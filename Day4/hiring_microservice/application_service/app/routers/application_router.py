from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.application_service import ApplicationService
from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationResponse,
)

router = APIRouter(prefix="/applications", tags=["Applications"])


def get_application_service(db: Session = Depends(get_db)):
    return ApplicationService(db)


@router.post("/", response_model=ApplicationResponse)
def apply_job(
    payload: ApplicationCreate,
    service: ApplicationService = Depends(get_application_service),
):
    return service.apply_job(payload)


@router.get("/user/{user_id}", response_model=list[ApplicationResponse])
def track_applications(
    user_id: int,
    service: ApplicationService = Depends(get_application_service),
):
    return service.track_applications(user_id)