import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.session import get_db

TEST_DB_URL = "sqlite:///./test_leave.db"
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


def get_token(email, password):
    response = client.post("/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def setup_users():
    """Create admin, manager, employee and a department"""
    # Admin
    client.post("/auth/register", json={"name": "Admin", "email": "admin@leave.com", "password": "admin123", "role": "ADMIN"})
    # Manager (dept 1)
    client.post("/auth/register", json={"name": "Manager", "email": "manager@leave.com", "password": "mgr123", "role": "MANAGER", "department_id": 1})
    # Employee (dept 1)
    client.post("/auth/register", json={"name": "Employee", "email": "emp@leave.com", "password": "emp123", "role": "EMPLOYEE", "department_id": 1})

    admin_token = get_token("admin@leave.com", "admin123")
    # Create department with manager
    client.post("/admin/departments", json={"name": "Engineering", "manager_id": 2},
                headers={"Authorization": f"Bearer {admin_token}"})
    return admin_token


def test_employee_apply_leave():
    setup_users()
    token = get_token("emp@leave.com", "emp123")
    response = client.post("/employee/leaves",
        json={"start_date": "2025-08-01", "end_date": "2025-08-03", "reason": "Vacation"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["reason"] == "Vacation"


def test_employee_apply_overlapping_leave():
    token = get_token("emp@leave.com", "emp123")
    # Apply first leave
    client.post("/employee/leaves",
        json={"start_date": "2025-09-10", "end_date": "2025-09-12", "reason": "Trip"},
        headers={"Authorization": f"Bearer {token}"}
    )
    # Apply overlapping
    response = client.post("/employee/leaves",
        json={"start_date": "2025-09-11", "end_date": "2025-09-13", "reason": "Another trip"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400


def test_manager_approve_leave():
    emp_token = get_token("emp@leave.com", "emp123")
    mgr_token = get_token("manager@leave.com", "mgr123")

    # Employee applies leave
    leave_resp = client.post("/employee/leaves",
        json={"start_date": "2025-10-01", "end_date": "2025-10-02", "reason": "Personal"},
        headers={"Authorization": f"Bearer {emp_token}"}
    )
    leave_id = leave_resp.json()["id"]

    # Manager approves
    response = client.patch(f"/manager/leaves/{leave_id}/status",
        json={"status": "APPROVED"},
        headers={"Authorization": f"Bearer {mgr_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


def test_unauthorized_employee_cannot_approve():
    emp_token = get_token("emp@leave.com", "emp123")

    leave_resp = client.post("/employee/leaves",
        json={"start_date": "2025-11-01", "end_date": "2025-11-02", "reason": "Rest"},
        headers={"Authorization": f"Bearer {emp_token}"}
    )
    leave_id = leave_resp.json()["id"]

    # Employee tries to approve (should fail)
    response = client.patch(f"/manager/leaves/{leave_id}/status",
        json={"status": "APPROVED"},
        headers={"Authorization": f"Bearer {emp_token}"}
    )
    assert response.status_code == 403


def test_admin_override_leave():
    emp_token = get_token("emp@leave.com", "emp123")
    admin_token = get_token("admin@leave.com", "admin123")

    leave_resp = client.post("/employee/leaves",
        json={"start_date": "2025-12-01", "end_date": "2025-12-03", "reason": "Holiday"},
        headers={"Authorization": f"Bearer {emp_token}"}
    )
    leave_id = leave_resp.json()["id"]

    response = client.patch(f"/admin/leaves/{leave_id}/status",
        json={"status": "REJECTED"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "REJECTED"