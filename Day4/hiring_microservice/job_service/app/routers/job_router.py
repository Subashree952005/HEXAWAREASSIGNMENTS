from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.job_service import JobService
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_job_service(db: Session = Depends(get_db)):
    return JobService(db)


@router.post("/", response_model=JobResponse)
def create_job(payload: JobCreate, service: JobService = Depends(get_job_service)):
    return service.create_job(payload)


@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, payload: JobUpdate, service: JobService = Depends(get_job_service)):
    return service.update_job(job_id, payload)


@router.get("/", response_model=list[JobResponse])
def list_jobs(service: JobService = Depends(get_job_service)):
    return service.list_jobs()