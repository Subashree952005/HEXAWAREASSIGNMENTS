import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.session import get_db

# Use in-memory SQLite for tests
TEST_DB_URL = "sqlite:///./test_elms.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_user():
    response = client.post("/auth/register", json={
        "name": "Test Admin",
        "email": "admin@test.com",
        "password": "admin123",
        "role": "ADMIN"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["role"] == "ADMIN"


def test_register_duplicate_email():
    # Register first
    client.post("/auth/register", json={
        "name": "User1",
        "email": "dup@test.com",
        "password": "pass123",
        "role": "EMPLOYEE"
    })
    # Try to register again with same email
    response = client.post("/auth/register", json={
        "name": "User2",
        "email": "dup@test.com",
        "password": "pass456",
        "role": "EMPLOYEE"
    })
    assert response.status_code == 400


def test_login_success():
    client.post("/auth/register", json={
        "name": "Login User",
        "email": "login@test.com",
        "password": "password123",
        "role": "EMPLOYEE"
    })
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials():
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_wrong_password():
    client.post("/auth/register", json={
        "name": "Pass Test",
        "email": "passtest@test.com",
        "password": "correctpass",
        "role": "EMPLOYEE"
    })
    response = client.post("/auth/login", json={
        "email": "passtest@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401