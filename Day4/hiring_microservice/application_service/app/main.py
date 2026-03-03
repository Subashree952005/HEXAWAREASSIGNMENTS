from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.routers.application_router import router

#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Application Service")

app.include_router(router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "Application Service Running on 8005"}