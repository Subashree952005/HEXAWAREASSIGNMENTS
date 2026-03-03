import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("eams")


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.warning(f"DB IntegrityError on {request.url.path}: {exc.orig}")
    return JSONResponse(status_code=400, content={"detail": "Data conflict or constraint violation"})