from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.company_schema import CompanyCreate, CompanyUpdate, CompanyResponse
from app.services import company_service

router = APIRouter()

@router.post("/", response_model=CompanyResponse)
def create(company: CompanyCreate, db: Session = Depends(get_db)):
    return company_service.create_company(db, company)

@router.get("/", response_model=list[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return company_service.get_companies(db)

@router.get("/{company_id}", response_model=CompanyResponse)
def get(company_id: int, db: Session = Depends(get_db)):
    company = company_service.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db)):
    company = company_service.update_company(db, company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/{company_id}")
def delete(company_id: int, db: Session = Depends(get_db)):
    company = company_service.delete_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Deleted successfully"}