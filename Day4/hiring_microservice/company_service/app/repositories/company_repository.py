from sqlalchemy.orm import Session
from app.models.company import Company

def create(db: Session, data: dict):
    company = Company(**data)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def get_by_id(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def get_all(db: Session):
    return db.query(Company).all()

def update(db: Session, company, update_data: dict):
    for key, value in update_data.items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    return company

def delete(db: Session, company):
    db.delete(company)
    db.commit()
    return company