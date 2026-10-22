import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import MembersRole
from database.models import Users, Companies


def create_company_json():
    return {
        "company": {
            "name": "Test Company Name",
            "description": "Test Company Description",
            "phone": "Test company Phone Number",
            "email": "company@example.com",
        },
        "owner": {
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
            "phone": "Test Owner's Phone Number",
        }
    }


@pytest.mark.asyncio
async def test_create_company_access(
        client: AsyncClient,
        db_session: AsyncSession,
        user: Users,
        access_token: str
) -> None:
    response = await client.post(
        "/api/v1/companies/",
        json=create_company_json(),
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data.get("company_id") == 1
    assert data.get("user_id") == 1
    assert data.get("message") == "Company created successfully"
    assert data.get("role") == MembersRole.OWNER


@pytest.mark.asyncio
async def test_create_company_failed(
        client: AsyncClient,
        db_session: AsyncSession,
        user: Users,
):
    response = await client.post(
        "/api/v1/companies/",
        json=create_company_json(),
        headers={"Authorization": f"Bearer access_token"}
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid token"


@pytest.mark.asyncio
async def test_get_company_access(
        client: AsyncClient,
        db_session: AsyncSession,
        company: Companies,
):
    response = await client.get(
        "/api/v1/companies/1",
    )
    response.raise_for_status()

    data = response.json()

    assert response.status_code == 200

    assert data.get("id") == 1
    assert data.get("name") == "Test Company"
    assert data.get("description") == "Test Company Description"
    assert data.get("phone") == "Test Phone Number"
    assert data.get("email") == "company@example.com"
    assert data.get("created_at")


@pytest.mark.asyncio
async def test_get_company_failed(
        client: AsyncClient,
        db_session: AsyncSession,
        company: Companies,
):
    response = await client.get(
        "/api/v1/companies/9999",
    )

    assert response.status_code == 404
    assert response.json().get("detail") == "Company not found"


@pytest.mark.asyncio
async def test_update_company_access(
        client: AsyncClient,
        db_session: AsyncSession,
        company: Companies,
        owner_token: str
):
    response = await client.patch(
        "/api/v1/companies/1",
        json={
            "name": "New Test Name",
            "description": "New Test Description"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    response.raise_for_status()

    assert response.status_code == 200

    data = response.json()

    assert data.get("company_id") == company.id
    assert data.get("message") == "Company updated successfully"


@pytest.mark.asyncio
async def test_delete_company_access(
        client: AsyncClient,
        db_session: AsyncSession,
        company: Companies,
        owner_token: str
):
    response = await client.delete(
        "/api/v1/companies/1",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    response.raise_for_status()

    data = response.json()

    assert response.status_code == 200

    assert data.get("id") == company.id
    assert data.get("count_of_members")
    assert data.get("message") == "The company has become inactive"