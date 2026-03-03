import pytest


@pytest.mark.asyncio
async def test_create_asset_as_itadmin(client, itadmin_token):
    res = await client.post(
        "/itadmin/assets",
        json={"asset_tag": "LT-TEST-001", "asset_type": "LAPTOP", "brand": "Dell", "model": "Latitude"},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 201
    assert res.json()["asset_tag"] == "LT-TEST-001"
    assert res.json()["status"] == "AVAILABLE"


@pytest.mark.asyncio
async def test_create_asset_as_superadmin(client, superadmin_token):
    res = await client.post(
        "/itadmin/assets",
        json={"asset_tag": "MON-TEST-001", "asset_type": "MONITOR", "brand": "LG"},
        headers={"Authorization": f"Bearer {superadmin_token}"}
    )
    assert res.status_code == 201
    assert res.json()["asset_type"] == "MONITOR"


@pytest.mark.asyncio
async def test_create_asset_duplicate_tag(client, itadmin_token):
    res = await client.post(
        "/itadmin/assets",
        json={"asset_tag": "LT-TEST-001", "asset_type": "LAPTOP"},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_asset_unauthorized_employee(client, employee_token):
    res = await client.post(
        "/itadmin/assets",
        json={"asset_tag": "LT-999", "asset_type": "LAPTOP"},
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_create_asset_unauthorized_manager(client, manager_token):
    res = await client.post(
        "/itadmin/assets",
        json={"asset_tag": "LT-998", "asset_type": "LAPTOP"},
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_list_assets(client, itadmin_token):
    res = await client.get(
        "/itadmin/assets",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert "items" in res.json()
    assert "total" in res.json()


@pytest.mark.asyncio
async def test_list_assets_filter_by_status(client, itadmin_token):
    res = await client.get(
        "/itadmin/assets?status=AVAILABLE",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    for item in res.json()["items"]:
        assert item["status"] == "AVAILABLE"


@pytest.mark.asyncio
async def test_get_asset_by_id(client, itadmin_token):
    res = await client.get(
        "/itadmin/assets/1",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["id"] == 1


@pytest.mark.asyncio
async def test_get_asset_not_found(client, itadmin_token):
    res = await client.get(
        "/itadmin/assets/99999",
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_update_asset(client, itadmin_token):
    res = await client.patch(
        "/itadmin/assets/1",
        json={"brand": "HP", "notes": "Updated brand"},
        headers={"Authorization": f"Bearer {itadmin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["brand"] == "HP"