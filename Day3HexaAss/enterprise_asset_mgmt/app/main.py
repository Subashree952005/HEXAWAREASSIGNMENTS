from app.models import user, department, asset, asset_assignment, asset_request, audit_log
import app.models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from app.middleware.logging import logging_middleware
from app.middleware.exception_handler import global_exception_handler, integrity_error_handler
from app.routers import auth_router, superadmin_router, itadmin_router, manager_router, employee_router

app = FastAPI(
    title="Enterprise Asset Management System",
    description="Centralized API for managing physical and digital company assets",
    version="1.0.0",
)

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Middleware ─────────────────────────────────────────────────────────────────
app.middleware("http")(logging_middleware)

# ─── Exception Handlers ────────────────────────────────────────────────────────
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)

# ─── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(superadmin_router.router)
app.include_router(itadmin_router.router)
app.include_router(manager_router.router)
app.include_router(employee_router.router)


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "Enterprise Asset Management System"}