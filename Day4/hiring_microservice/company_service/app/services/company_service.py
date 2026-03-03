from sqlalchemy.orm import Session
from app.repositories.company_repository import (
    create_company,
    get_all_companies,
    get_company_by_id,
    delete_company
)


def create_company_service(db: Session, company):
    return create_company(db, company.dict())


def list_companies_service(db: Session):
    return get_all_companies(db)


def delete_company_service(db: Session, company_id: int):
    company = get_company_by_id(db, company_id)
    if not company:
        raise Exception("Company not found")

    delete_company(db, company)
    return {"message": "Company deleted successfully"}