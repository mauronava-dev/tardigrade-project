"""Shared test fixtures for Tardigrade test suite.

This module provides common fixtures used across unit and integration tests.
"""

import asyncio
from collections.abc import AsyncGenerator, Generator
from datetime import datetime
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.domain.entities.user import User
from src.infrastructure.database.base import Base
from src.main import app


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# In-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_engine():
    """Create an async database engine for testing."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create an isolated database session for tests.

    Each test gets a fresh session that is rolled back after the test.
    """
    session_factory = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Async test client for FastAPI.

    Provides an HTTP client for testing API endpoints.
    """
    from src.infrastructure.database.base import get_session

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# Sample data fixtures
@pytest.fixture
def sample_user_data() -> dict[str, Any]:
    """Provide sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
    }


@pytest.fixture
def sample_user() -> User:
    """Provide a sample User domain entity."""
    return User(
        id=1,
        email="test@example.com",
        name="Test User",
        is_active=True,
        created_at=datetime.now(),
    )


@pytest.fixture
def invalid_user_data_missing_email() -> dict[str, Any]:
    """Provide invalid user data with missing email."""
    return {
        "name": "Test User",
    }


@pytest.fixture
def invalid_user_data_short_name() -> dict[str, Any]:
    """Provide invalid user data with short name."""
    return {
        "email": "test@example.com",
        "name": "A",
    }
