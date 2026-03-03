from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.models.company import Company
from app.routers.company_router import router as company_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company Service")

app.include_router(company_router, prefix="/companies", tags=["Companies"])