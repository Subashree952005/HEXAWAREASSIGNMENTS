from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.department_repo import dept_repo
from app.repositories.user_repo import user_repo
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate

class DepartmentService:
    def get_department(self, db: Session, dept_id: int):
        dept = dept_repo.get_by_id(db, dept_id)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
        return dept

    def get_all(self, db: Session, offset: int, limit: int):
        return dept_repo.get_all(db, offset, limit)

    def create_department(self, db: Session, data: DepartmentCreate):
        if data.manager_id:
            manager = user_repo.get_by_id(db, data.manager_id)
            if not manager:
                raise HTTPException(status_code=404, detail="Manager not found")
        return dept_repo.create(db, data)

    def update_department(self, db: Session, dept_id: int, data: DepartmentUpdate):
        dept = self.get_department(db, dept_id)
        return dept_repo.update(db, dept, data)

    def delete_department(self, db: Session, dept_id: int):
        dept = self.get_department(db, dept_id)
        dept_repo.delete(db, dept)
        return {"message": "Department deleted"}

dept_service = DepartmentService()