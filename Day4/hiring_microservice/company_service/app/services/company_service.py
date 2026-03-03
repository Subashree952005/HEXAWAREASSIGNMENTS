from sqlalchemy.orm import Session
from app.schemas.company_schema import CompanyCreate, CompanyUpdate
from app.repositories import company_repository

def create_company(db: Session, company: CompanyCreate):
    return company_repository.create(db, company.model_dump())

def get_company(db: Session, company_id: int):
    return company_repository.get_by_id(db, company_id)

def get_companies(db: Session):
    return company_repository.get_all(db)

def update_company(db: Session, company_id: int, data: CompanyUpdate):
    company = company_repository.get_by_id(db, company_id)
    if not company:
        return None

    update_data = data.model_dump(exclude_unset=True)
    return company_repository.update(db, company, update_data)

def delete_company(db: Session, company_id: int):
    company = company_repository.get_by_id(db, company_id)
    if not company:
        return None

    return company_repository.delete(db, company)