from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.application_repository import ApplicationRepository
from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationResponse,
)


class ApplicationService:

    def __init__(self, db: Session):
        self.repo = ApplicationRepository(db)

    def apply_job(self, payload: ApplicationCreate) -> ApplicationResponse:
        application = self.repo.create_application(payload.model_dump())
        return ApplicationResponse.model_validate(application)

    def track_applications(self, user_id: int):
        applications = self.repo.get_applications_by_user(user_id)
        return [
            ApplicationResponse.model_validate(app)
            for app in applications
        ]