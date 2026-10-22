from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.config import get_async_session
from database.models import Base, Companies, Users, MembersRole, UsersToken, CompanyMembers
from cache.redis import redis
from main import app
from modules.companies.repo import CompanyRepo
from modules.companies.service import CompanyService
from utils.security.password import hashed_password
from utils.security.token import create_invitation_token

TEST_DATABASE_URL=(
        "postgresql+asyncpg://postgres:postgres@localhost:5434/service_flow_test"
)

test_engine = create_async_engine(TEST_DATABASE_URL)

test_session = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


@pytest_asyncio.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> Users:
    user = Users(
        email="user@example.com",
        password_hash=hashed_password("Test Password"),
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def company(db_session: AsyncSession, user: Users) -> Companies:
    company = Companies(
        name="Test Company",
        description="Test Company Description",
        phone="Test Phone Number",
        email="company@example.com",
        user_id=user.id
    )

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    return company


@pytest_asyncio.fixture
async def worker(
        db_session: AsyncSession,
        company: Companies
) -> CompanyMembers:
    user = Users(
        email="employee@example.com",
        password_hash=hashed_password("Test Password"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    worker = CompanyMembers(
        company_id=company.id,
        user_id=user.id,
        role=MembersRole.WORKER,
        first_name="Test Name",
        last_name="Test Name",
        phone="Test Worker Phone Number",
    )

    db_session.add(worker)
    await db_session.commit()
    await db_session.refresh(worker)

    return worker


@pytest_asyncio.fixture
async def owner(
        db_session: AsyncSession,
        user: Users,
        company: Companies
) -> CompanyMembers:
    owner = CompanyMembers(
        company_id=company.id,
        user_id=user.id,
        role=MembersRole.OWNER,
        first_name="Test Name",
        last_name="Test Name",
        phone="Test Owner Phone Number",
    )

    db_session.add(owner)
    await db_session.commit()
    await db_session.refresh(owner)

    return owner


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_new_session():
        async with test_session() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_new_session

    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app)
    ) as client:
        yield client

    app.dependency_overrides.clear()
    await redis.aclose()


@pytest_asyncio.fixture
async def owner_token(
        client: AsyncClient,
        user: Users,
        owner: CompanyMembers
) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user.email,
            "password": "Test Password"
        }
    )

    assert response.status_code == 200

    return response.json().get("access_token")


@pytest.fixture
async def access_token(client: AsyncClient, db_session: AsyncSession, user: Users) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "Test Password"
        }
    )

    assert response.status_code == 200, response.text
    access_token = response.json()["access_token"]

    assert access_token

    return access_token

@pytest_asyncio.fixture
async def token(db_session: AsyncSession, worker: CompanyMembers) -> str:
    uuid_token, token_hash, expired_at = create_invitation_token()

    token = UsersToken(
        user_id=worker.user_id,
        token_hash=token_hash,
        used=False,
        expired_at=datetime.now(timezone.utc) + timedelta(seconds=10),
    )

    db_session.add(token)
    await db_session.commit()
    await db_session.refresh(token)

    return uuid_token
