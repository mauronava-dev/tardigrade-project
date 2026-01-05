# GitHub Copilot Instructions

You are an AI assistant helping developers work on the Tardigrade Project, a Python backend template following hexagonal architecture.

## Project Context

- **Stack**: Python 3.12, FastAPI, SQLAlchemy, Alembic, Docker, Terraform
- **Architecture**: Hexagonal (ports and adapters)
- **Databases**: PostgreSQL, MySQL, DynamoDB, Redis, MongoDB, Redshift
- **AI Integration**: Amazon Bedrock for chatbots and agents

## Code Standards

### Language & Naming
- All code, comments, and documentation in English
- `snake_case` for variables, functions, file names
- `PascalCase` for class names
- `UPPER_SNAKE_CASE` for constants

### Formatting
- Line length: 120 characters
- Indentation: 4 spaces
- String quotes: double quotes (`"`)
- Type hints required on all function signatures

### Documentation
- Google-style docstrings for all public functions, classes, and modules
- Include Args, Returns, and Raises sections

```python
def calculate_total(items: list[dict], tax_rate: float) -> float:
    """
    Calculate total price including tax.

    Args:
        items: List of items with 'price' and 'quantity' keys.
        tax_rate: Tax rate as decimal (e.g., 0.16 for 16%).

    Returns:
        Total price including tax.

    Raises:
        ValueError: If tax_rate is negative.
    """
```

## Architecture Rules

### Directory Structure
```
src/
├── domain/           # Business logic (NO external dependencies)
│   ├── entities/     # Domain models
│   ├── services/     # Domain services
│   └── exceptions/   # Domain exceptions
├── application/      # Use cases and ports
│   ├── use_cases/    # Application logic
│   └── interfaces/   # Port definitions (abstract classes)
├── infrastructure/   # External adapters
│   ├── database/     # SQL, DynamoDB, Redis, MongoDB
│   ├── api/          # FastAPI routes and schemas
│   └── external/     # Third-party integrations
└── shared/           # Utilities and constants
```

### Dependency Direction
- Domain has NO external dependencies
- Application orchestrates domain logic
- Infrastructure adapts external systems
- Dependencies point inward: infrastructure → application → domain

## SQL Query Optimization

Always follow: **Filter → Project → Aggregate → Join → Order**

### Required Patterns
```python
# ✅ Select only needed columns
query = select(User.id, User.email).where(User.active == True)

# ✅ Filter early with subquery
filtered = select(Order.customer_id, func.sum(Order.amount).label("total"))
    .where(Order.created_at >= start_date)
    .group_by(Order.customer_id)
    .subquery()

# ✅ Use EXISTS instead of IN
query = select(Customer).where(exists(
    select(Order.id).where(Order.customer_id == Customer.id)
))

# ✅ Batch operations
await session.execute(insert(User), users_list)
```

### Avoid
- `SELECT *` - always specify columns
- Functions on indexed columns in WHERE clauses
- `DISTINCT` without necessity
- N+1 query patterns

## Testing Requirements

- Minimum 80% code coverage
- Use pytest with pytest-asyncio
- Mirror source structure in tests/

```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test user creation endpoint."""
    response = await client.post("/api/v1/users", json={"email": "test@example.com"})
    assert response.status_code == 201
```

## FastAPI Patterns

```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: str = Field(..., example="user@example.com")
    name: str = Field(..., min_length=2, max_length=100)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user."""
    pass
```

## Environment Variables

Always use `os.getenv()` with defaults:

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://localhost:5432/dev")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

## Authentication

JWT-based with access (15min) and refresh (7 days) tokens:

```python
from fastapi import Depends
from infrastructure.api.auth import get_current_user

@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return user
```

## Repository Pattern

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: str) -> T | None:
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
```

## Additional Context

Check `docs/user/` directory for project-specific documentation that may contain business rules, API specs, or integration guides.
