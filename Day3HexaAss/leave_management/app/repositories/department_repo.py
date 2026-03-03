from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate

class DepartmentRepository:
    def get_by_id(self, db: Session, dept_id: int):
        return db.query(Department).filter(Department.id == dept_id).first()

    def get_all(self, db: Session, offset: int = 0, limit: int = 10):
        total = db.query(Department).count()
        items = db.query(Department).offset(offset).limit(limit).all()
        return total, items

    def create(self, db: Session, data: DepartmentCreate):
        dept = Department(name=data.name, manager_id=data.manager_id)
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    def update(self, db: Session, dept: Department, data: DepartmentUpdate):
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(dept, field, value)
        db.commit()
        db.refresh(dept)
        return dept

    def delete(self, db: Session, dept: Department):
        db.delete(dept)
        db.commit()

dept_repo = DepartmentRepository()