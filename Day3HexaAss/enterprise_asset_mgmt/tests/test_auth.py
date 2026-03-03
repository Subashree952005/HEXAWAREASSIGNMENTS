import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_login_superadmin(client):
    res = await client.post("/auth/login", data={"username": "superadmin@company.com", "password": "admin123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_login_itadmin(client):
    res = await client.post("/auth/login", data={"username": "itadmin@company.com", "password": "admin123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    res = await client.post("/auth/login", data={"username": "superadmin@company.com", "password": "wrongpass"})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_login_wrong_email(client):
    res = await client.post("/auth/login", data={"username": "nobody@company.com", "password": "admin123"})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, superadmin_token):
    res = await client.get("/auth/me", headers={"Authorization": f"Bearer {superadmin_token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "superadmin@company.com"
    assert res.json()["role"] == "SUPERADMIN"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    res = await client.get("/auth/me")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_me_invalid_token(client):
    res = await client.get("/auth/me", headers={"Authorization": "Bearer invalidtoken123"})
    assert res.status_code == 401