import pytest


INVITATION_URL = "/api/v1/auth/employees/invitations"


def invitation_payload(email: str = "employee@example.com") -> dict[str, str]:
    return {
        "email": email,
        "password": "Temporary password",
        "first_name": "Test",
        "last_name": "Employee",
        "phone": "+79123456789",
        "role": "WORKER",
    }


@pytest.mark.asyncio
async def test_register_new_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "password": "Test Password",
            "retry_password": "Test Password"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Successfully registered new user"
    assert response.json()["user_id"] == 1
    assert response.json()["email"] == "user@example.com"


@pytest.mark.asyncio
async def test_invalid_register_new_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "password": "pass",
            "retry_password": "pass"
        }
    )
    print(response.json())
    assert response.status_code == 422

    detail = response.json()["detail"][0]

    assert detail["loc"] == ["body", "password"]
    assert "Password must be at least 8 characters" in detail.get("msg")


@pytest.mark.asyncio
async def test_create_employee_invitation(client, owner_token: str):
    response = await client.post(
        INVITATION_URL,
        json=invitation_payload(),
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Employee created"
    assert response.json()["token"].endswith("/activate")


@pytest.mark.asyncio
async def test_create_employee_invitation_for_registered_email_returns_conflict(
        client, owner_token: str
):
    payload = invitation_payload()
    headers = {"Authorization": f"Bearer {owner_token}"}

    first_response = await client.post(INVITATION_URL, json=payload, headers=headers)
    response = await client.post(INVITATION_URL, json=payload, headers=headers)

    assert first_response.status_code == 201
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_activate_employee_invitation(client, owner_token: str):
    invitation = await client.post(
        INVITATION_URL,
        json=invitation_payload(),
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    token = invitation.json()["token"].removeprefix("/employees/invitations/").removesuffix("/activate")

    response = await client.post(
        f"{INVITATION_URL}/{token}/activate",
        json={
            "new_password": "New test password",
            "new_password_confirm": "New test password",
        },
    )

    assert invitation.status_code == 201
    assert response.status_code == 200
    assert response.json()["message"] == "Employee activated"


@pytest.mark.asyncio
async def test_activate_employee_invitation_with_invalid_token(client):
    response = await client.post(
        f"{INVITATION_URL}/invalid-token/activate",
        json={
            "new_password": "New test password",
            "new_password_confirm": "New test password",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_login_returns_access_token(client, user, owner):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "Test Password"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
