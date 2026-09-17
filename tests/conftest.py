from datetime import datetime, timedelta, timezone

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database.config import get_async_session
from app.database.models import Base, Companies, Users, UserRole, UsersToken
from app.main import app
from app.utils.security.password import hashed_password
from app.utils.security.token import create_invitation_token

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
async def owner(db_session: AsyncSession, company: Companies):
    user = Users(
        company_id=company.id,
        email="user@example.com",
        password_hash=hashed_password("Test Password"),
        role=UserRole.OWNER
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_new_session():
        async with test_session() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_new_session

async def company(db_session):
    company = Companies(
        name="Test Company",
        description="Test Company description",
        phone="+7 912 345 6789",
        email="example@example.com",
    )

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    return company


@pytest_asyncio.fixture
async def owner(db_session: AsyncSession, company: Companies):
    user = Users(
        company_id=company.id,
        email="user@example.com",
        password_hash=hashed_password("Test Password"),
        role=UserRole.OWNER
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


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


@pytest_asyncio.fixture
async def owner_token(client: AsyncClient, owner):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": owner.email,
            "password": "Test Password"
        }
    )

    assert response.status_code == 200

    return response.json().get("access_token")


@pytest_asyncio.fixture
async def token(db_session: AsyncSession, owner: Users):
    uuid_token, token_hash, expired_at = create_invitation_token()

    token = UsersToken(
        user_id=owner.id,
        token_hash=token_hash,
        used=False,
        expired_at=datetime.now(timezone.utc) + timedelta(seconds=10),
    )

    db_session.add(token)
    await db_session.commit()
    await db_session.refresh(token)

    return uuid_token


@pytest_asyncio.fixture
async def owner_token(client: AsyncClient, owner):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": owner.email,
            "password": "Test Password"
        }
    )

    assert response.status_code == 200

    return response.json().get("access_token")