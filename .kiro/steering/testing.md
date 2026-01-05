# Testing Guidelines

## Stack

- pytest as test framework
- pytest-asyncio for async tests
- pytest-cov for coverage (80% minimum)
- httpx for FastAPI test client
- factory_boy for test data

## Directory Structure

```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests (no external dependencies)
│   ├── domain/
│   └── application/
├── integration/          # Tests with database/services
│   └── infrastructure/
└── factories/            # Test data factories
```

## FastAPI Test Pattern

```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
async def client():
    """Async test client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation endpoint."""
    response = await client.post("/api/v1/users", json={"email": "test@example.com"})
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Database Fixtures

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
async def db_session():
    """Create isolated database session for tests."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
```

## Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html --cov-fail-under=80

# Run specific test file
pytest tests/unit/domain/test_user.py -v
```
