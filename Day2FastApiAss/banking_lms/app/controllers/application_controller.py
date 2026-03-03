from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate
)
from app.services.application_service import ApplicationService
print("APPLICATION CONTROLLER LOADED")
router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    return ApplicationService.create_application(db, data)

@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    current_user_id: int,
    db: Session = Depends(get_db)
):
    return ApplicationService.update_status(
        db,
        application_id,
        status_update,
        current_user_id
    )