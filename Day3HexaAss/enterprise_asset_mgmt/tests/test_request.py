import pytest


@pytest.mark.asyncio
async def test_employee_create_request(client, employee_token):
    res = await client.post(
        "/employee/requests",
        json={"asset_type": "LAPTOP", "reason": "Need for remote work"},
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert res.status_code == 201
    assert res.json()["status"] == "PENDING"
    assert res.json()["asset_type"] == "LAPTOP"


@pytest.mark.asyncio
async def test_employee_view_own_requests(client, employee_token):
    res = await client.get(
        "/employee/requests",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert res.status_code == 200
    assert "items" in res.json()


@pytest.mark.asyncio
async def test_itadmin_list_requests(client, itadmin_token):
    res = await client.get(
        "/itadmin/requests",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert "items" in res.json()


@pytest.mark.asyncio
async def test_itadmin_list_pending_requests(client, itadmin_token):
    res = await client.get(
        "/itadmin/requests?status=PENDING",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    for item in res.json()["items"]:
        assert item["status"] == "PENDING"


@pytest.mark.asyncio
async def test_reject_request(client, itadmin_token):
    res = await client.post(
        "/itadmin/requests/1/reject",
        json={"rejection_reason": "No stock available"},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["status"] == "REJECTED"


@pytest.mark.asyncio
async def test_approve_already_rejected_request(client, itadmin_token):
    res = await client.post(
        "/itadmin/requests/1/approve",
        json={"asset_id": 1},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_employee_cannot_approve(client, employee_token):
    res = await client.post(
        "/itadmin/requests/1/approve",
        json={"asset_id": 1},
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert res.status_code == 403