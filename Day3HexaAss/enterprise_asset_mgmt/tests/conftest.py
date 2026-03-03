import pytest
import anyio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
async def superadmin_token(client):
    res = await client.post("/auth/login", data={"username": "superadmin@company.com", "password": "admin123"})
    return res.json()["access_token"]


@pytest.fixture
async def itadmin_token(client):
    res = await client.post("/auth/login", data={"username": "itadmin@company.com", "password": "admin123"})
    return res.json()["access_token"]


@pytest.fixture
async def manager_token(client):
    res = await client.post("/auth/login", data={"username": "manager@company.com", "password": "admin123"})
    return res.json()["access_token"]


@pytest.fixture
async def employee_token(client):
    res = await client.post("/auth/login", data={"username": "employee@company.com", "password": "admin123"})
    return res.json()["access_token"]