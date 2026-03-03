from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.controllers.loan_controller import router as loan_router

app = FastAPI(title="Loan Application API")

add_cors_middleware(app)

app.include_router(loan_router, prefix="/loans", tags=["Loans"])

@app.get("/")
def root():
    return {"message": "Loan API running"}
