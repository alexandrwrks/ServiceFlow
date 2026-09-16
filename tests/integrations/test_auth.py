import pytest

from app.database.models import UserRole

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


@pytest.mark.asyncio
async def test_employees_invitations_access(client, owner_token):
    request_schema = {
        "first_name": "Test Employees",
        "last_name": "Test Employees",
        "phone": "+7 912 345 6789",
        "email": "example@example.com",
        "password": "Test Password",
        "role": UserRole.EMPLOYEE,
    }

    response = await client.post(
        "/api/v1/auth/employees/invitations",
        json=request_schema,
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert data.get("message") == "Employee created"


@pytest.mark.asyncio
async def test_employee_invitations_failed(client, owner_token, owner):
    request_schema = {
        "first_name": "Test Employees",
        "last_name": "Test Employees",
        "phone": "+7 912 345 6789",
        "email": "user@example.com",
        "password": "Test Password",
        "role": UserRole.EMPLOYEE,
    }

    response = await client.post(
        "/api/v1/auth/employees/invitations",
        json=request_schema,
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    assert response.status_code == 409

    data = response.json()

    assert data.get("detail") == "Email already registered"


@pytest.mark.asyncio
async def test_accept_employee_invitations_access(client, token):
    response = await client.post(
        f"/api/v1/auth/employees/invitations/{token}/activate",
        json={
            "new_password": "Test Password",
            "new_password_confirm": "Test Password"
        }
    )

    assert response.status_code == 200
    assert response.json().get("message") == "Employee activated"


@pytest.mark.asyncio
async def test_accept_employee_invitations_failed(client):
    response = await client.post(
        f"/api/v1/auth/employees/invitations/token/activate",
        json={
            "new_password": "Test Password",
            "new_password_confirm": "Test Password"
        }
    )

    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid token"


@pytest.mark.asyncio
async def test_login_accept(client, owner):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": owner.email,
            "password": "Test Password",
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data