import pytest
from datetime import date


@pytest.mark.asyncio
async def test_assign_asset(client, itadmin_token):
    res = await client.post(
        "/itadmin/assignments",
        json={"asset_id": 1, "user_id": 4, "assigned_date": str(date.today())},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 201
    assert res.json()["is_active"] is True
    assert res.json()["asset_id"] == 1


@pytest.mark.asyncio
async def test_assign_already_assigned_asset(client, itadmin_token):
    res = await client.post(
        "/itadmin/assignments",
        json={"asset_id": 1, "user_id": 3, "assigned_date": str(date.today())},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_employee_view_own_assets(client, employee_token):
    res = await client.get(
        "/employee/my-assets",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_list_assignments(client, itadmin_token):
    res = await client.get(
        "/itadmin/assignments",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert "items" in res.json()


@pytest.mark.asyncio
async def test_return_asset(client, itadmin_token):
    res = await client.post(
        "/itadmin/assignments/1/return",
        json={"returned_date": str(date.today()), "condition_on_return": "GOOD"},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["is_active"] is False


@pytest.mark.asyncio
async def test_return_already_returned_asset(client, itadmin_token):
    res = await client.post(
        "/itadmin/assignments/1/return",
        json={"returned_date": str(date.today()), "condition_on_return": "GOOD"},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 400