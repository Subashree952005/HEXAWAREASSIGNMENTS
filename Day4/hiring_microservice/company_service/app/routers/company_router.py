from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.company_schema import CompanyCreate, CompanyResponse
from app.services.company_service import (
    create_company_service,
    list_companies_service,
    delete_company_service
)
from app.database.session import get_db

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return create_company_service(db, company)


@router.get("/", response_model=List[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return list_companies_service(db)


@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    try:
        return delete_company_service(db, company_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))