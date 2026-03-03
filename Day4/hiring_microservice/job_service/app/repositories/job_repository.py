from sqlalchemy.orm import Session
from app.models.job import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job_data: dict) -> Job:
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job_by_id(self, job_id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_all_jobs(self):
        return self.db.query(Job).all()

    def update_job(self, job: Job, update_data: dict) -> Job:
        for key, value in update_data.items():
            setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        return job