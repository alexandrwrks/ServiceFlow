import pytest


@pytest.mark.asyncio
async def test_get_company_access(client):
    response = await client.get("/api/v1/companies/1")

    assert response.status_code == 200

    data = response.json()

    assert data.get("id") == 1

    assert "email" in data
    assert "name" in data
    assert "phone" in data
    assert "description" in data


@pytest.mark.asyncio
async def test_get_company_failed(client):
    response = await client.get("/api/v1/companies/-1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}


@pytest.mark.asyncio
async def test_create_company_access(client):
    new_company = {
        "title": "Company",
        "description": "Description",
        "phone": "+7 912 345 67 89",
        "email": "example@gmail.com",
    }

    response = await client.post(
        "/api/v1/companies",
        json=new_company,
    )

    assert response.status_code == 200

    data = response.json()

    assert data.get("message") == "Company created successfully"

    assert "id" in data


@pytest.mark.asyncio
async def test_create_company_failed(client):
    new_company = {
        "title": "Company",
        "description": "Description",
        "phone": "+7 912 345 67 89",
        "email": "examplegmail.com",
    }

    response = await client.post(
        "/api/v1/companies",
        json=new_company,
    )

    assert response.status_code == 422

    data = response.json()

    assert (
        data.get("detail")[0].get("msg")
        == "value is not a valid email address: An email address must have an @-sign."
    )


@pytest.mark.asyncio
async def test_update_company_access(client):
    company_id = 1

    new_company = {
        "title": "Company",
        "description": "Description",
        "phone": "+7 912 345 67 89",
        "email": "example@gmail.com",
    }

    response = await client.patch(
        f"/api/v1/companies/{company_id}",
        json=new_company,
    )

    assert response.status_code == 200

    data = response.json()

    assert data.get("message") == "Company updated successfully"

    assert "id" in data


@pytest.mark.asyncio
async def test_update_company_failed(client):
    company_id = -1

    new_company = {
        "title": "Company",
        "description": "Description",
        "phone": "+7 912 345 67 89",
        "email": "example@gmail.com",
    }

    response = await client.patch(
        f"/api/v1/companies/{company_id}",
        json=new_company,
    )

    assert response.status_code == 404

    assert response.json().get("detail") == "Company not found"


@pytest.mark.asyncio
async def test_delete_company_access(client):
    company_id = 1

    response = await client.delete(
        f"/api/v1/companies/{company_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data.get("message") == "Company deleted successfully"
    assert "id" in data


@pytest.mark.asyncio
async def test_delete_company_failed(client):
    company_id = -1

    response = await client.delete(
        f"/api/v1/companies/{company_id}",
    )

    assert response.status_code == 404

    assert response.json().get("detail") == "Company not found"
