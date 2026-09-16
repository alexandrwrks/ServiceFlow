import pytest

company_request = {
    "company": {
        "name": "Test Company",
        "description": "Test Company Description",
        "phone": "+7 912 345 6789",
        "email": "example@example.com",
    },
    "owner": {
        "first_name": "Test Owner",
        "last_name": "Test Owner",
        "email": "example@example.com",
        "password": "Test Password"
    }
}


@pytest.mark.asyncio
async def test_register_company_access(client):
    response = await client.post(
        "/api/v1/auth/register-company",
        json=company_request
    )

    assert response.status_code == 200

    data = response.json()

    assert data.get("company_id") == 1
    assert data.get("message") == "Company created"


@pytest.mark.asyncio
async def test_register_company_failed(client, company):
    response = await client.post(
        "/api/v1/auth/register-company",
        json=company_request
    )

    assert response.status_code == 409

    data = response.json()

    assert data.get("detail") == "Email already registered"