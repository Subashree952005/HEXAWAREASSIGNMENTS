from fastapi import APIRouter, Request
import httpx
from app.core.config import settings

router = APIRouter()

SERVICE_MAP = {
    "auth": settings.AUTH_SERVICE_URL,
    "user": settings.USER_SERVICE_URL,
    "job": settings.JOB_SERVICE_URL,
    "company": settings.COMPANY_SERVICE_URL,
    "application": settings.APPLICATION_SERVICE_URL,
}

@router.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_MAP:
        return {"error": "Service not found"}

    target_url = f"{SERVICE_MAP[service]}/{path}"
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=request.headers.raw,
            content=await request.body()
        )

    return response.json()  