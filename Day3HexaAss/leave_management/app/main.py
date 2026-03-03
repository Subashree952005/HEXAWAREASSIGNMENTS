from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from app.database.base import Base
from app.database.session import engine
from app.middleware.logging import logging_middleware
from app.middleware.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)

# Import models to register with SQLAlchemy


from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.manager_router import router as manager_router
from app.routers.employee_router import router as employee_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Leave Management System",
    description="RBAC-based Leave Management API with JWT Auth",
    version="1.0.0"
)

# ─── Middleware ────────────────────────────────────────────────────────────────
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── Exception Handlers ───────────────────────────────────────────────────────
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(employee_router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "ELMS API is running 🚀", "docs": "/docs"}