from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.job_repository import JobRepository
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse


class JobService:

    def __init__(self, db: Session):
        self.repo = JobRepository(db)

    def create_job(self, payload: JobCreate) -> JobResponse:
        job = self.repo.create_job(payload.model_dump())
        return JobResponse.model_validate(job)

    def update_job(self, job_id: int, payload: JobUpdate) -> JobResponse:
        job = self.repo.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        update_data = payload.model_dump(exclude_unset=True)
        updated = self.repo.update_job(job, update_data)
        return JobResponse.model_validate(updated)

    def list_jobs(self):
        jobs = self.repo.get_all_jobs()
        return [JobResponse.model_validate(job) for job in jobs]