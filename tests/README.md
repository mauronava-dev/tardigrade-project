# Testing Structure

## Description

This directory contains all tests for the Tardigrade project, organized following the hexagonal architecture pattern.

## Directory Structure

```
tests/
├── conftest.py                    # Shared fixtures for all tests
├── README.md                      # This file
├── unit/                          # Unit tests (no external dependencies)
│   ├── domain/                    # Domain layer tests
│   │   └── test_user_entity.py    # User entity validation tests
│   ├── application/               # Application layer tests
│   │   └── test_user_use_cases.py # Use case tests
│   └── infrastructure/            # Infrastructure unit tests
│       └── test_repository_compliance.py
├── integration/                   # Integration tests (with database/services)
│   └── infrastructure/
│       └── test_user_api.py       # API endpoint tests
└── factories/                     # Test data factories
    └── user_factory.py            # User test data factory
```

## Test Types

### Unit Tests

Located in `tests/unit/`, these tests:
- Have no external dependencies (database, network, etc.)
- Test individual components in isolation
- Use mocks/stubs for dependencies when needed
- Run fast and can be executed frequently

### Integration Tests

Located in `tests/integration/`, these tests:
- Test multiple components working together
- Use an in-memory SQLite database for isolation
- Test API endpoints with real HTTP requests
- Verify database operations and transactions

### Property-Based Tests

Using Hypothesis library, these tests:
- Generate random inputs to find edge cases
- Run 100+ iterations per property
- Validate universal properties across all inputs
- Are tagged with feature and property references

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-fail-under=80

# Run specific test file
pytest tests/unit/domain/test_user_entity.py -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run with verbose output
pytest -v --tb=short

# Run property-based tests with more examples
pytest --hypothesis-show-statistics
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

| Fixture | Description |
|---------|-------------|
| `db_engine` | Async SQLAlchemy engine with in-memory SQLite |
| `db_session` | Isolated database session (rolled back after test) |
| `client` | Async HTTP client for API testing |
| `sample_user_data` | Sample user creation data |
| `sample_user` | Sample User domain entity |

## Test Factories

Test factories use `factory_boy` to generate test data:

```python
from tests.factories.user_factory import UserFactory

# Create a user with default values
user = UserFactory.build()

# Create a user with custom values
user = UserFactory.build(email="custom@example.com")

# Create multiple users
users = UserFactory.build_batch(5)
```

## Writing Tests

### Unit Test Example

```python
import pytest
from src.domain.entities.user import User
from src.domain.exceptions import InvalidEmailError


def test_user_validation_invalid_email():
    """Test that invalid email raises exception."""
    user = User(id=None, email="invalid", name="Test User")
    with pytest.raises(InvalidEmailError):
        user.validate()
```

### Integration Test Example

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation endpoint."""
    response = await client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

### Property-Based Test Example

```python
from hypothesis import given, settings, strategies as st
from src.domain.entities.user import User


@settings(max_examples=100)
@given(email=st.emails(), name=st.text(min_size=2, max_size=100))
def test_valid_user_passes_validation(email: str, name: str):
    """For any valid email and name, validation should pass."""
    user = User(id=None, email=email, name=name)
    user.validate()  # Should not raise
```

## Coverage Requirements

- Minimum coverage: 80%
- Coverage report generated in `htmlcov/` directory
- Excluded from coverage:
  - `__init__.py` files
  - Test files themselves
  - Type checking blocks

## Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Clarity**: Test names should describe what is being tested
3. **Single Responsibility**: Each test should verify one behavior
4. **Fast Execution**: Unit tests should run quickly
5. **Deterministic**: Tests should produce the same result every time
6. **Documentation**: Include docstrings explaining the test purpose
