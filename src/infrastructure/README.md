# Infrastructure Layer

## Description

The infrastructure layer contains adapters that connect the application to external systems. This includes database implementations, API routes, and external service integrations. Following hexagonal architecture, this layer implements the ports defined in the application layer.

## Business Rules

- All database operations must go through repository implementations
- API routes must use use cases from the application layer
- External service calls must be wrapped in adapters
- Authentication is handled via JWT tokens
- All API responses follow consistent error handling patterns

## Dependencies

- Internal: `src.application`, `src.domain`
- External: `fastapi`, `sqlalchemy`, `python-jose`, `pydantic`

## Directory Structure

```
infrastructure/
├── __init__.py
├── README.md
├── api/                      # FastAPI API layer
│   ├── __init__.py
│   ├── auth.py               # JWT authentication dependencies
│   ├── routes/               # API route definitions
│   │   ├── __init__.py
│   │   └── user_routes.py    # User CRUD endpoints
│   └── schemas/              # Pydantic request/response schemas
│       ├── __init__.py
│       └── user_schemas.py   # User schemas
├── database/                 # Database adapters
│   ├── __init__.py
│   ├── base.py               # SQLAlchemy base configuration
│   ├── sql/                  # SQL database implementations
│   │   ├── __init__.py
│   │   ├── models/           # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   └── user.py       # User model
│   │   └── repositories/     # Repository implementations
│   │       ├── __init__.py
│   │       └── user_repository.py
│   ├── dynamodb/             # DynamoDB implementations
│   │   └── __init__.py
│   ├── redis/                # Redis cache implementations
│   │   └── __init__.py
│   └── mongo/                # MongoDB implementations
│       └── __init__.py
└── external/                 # External service adapters
    ├── __init__.py
    └── bedrock/              # Amazon Bedrock adapter
        └── __init__.py
```

## Components

### API Layer (`api/`)

#### Authentication (`auth.py`)

JWT-based authentication with access and refresh tokens:

```python
from src.infrastructure.api.auth import get_current_user

@router.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"user_id": user["user_id"]}
```

#### Routes (`routes/`)

FastAPI routers for API endpoints. Each router:
- Uses dependency injection for database sessions
- Delegates business logic to use cases
- Returns Pydantic response models

#### Schemas (`schemas/`)

Pydantic models for request validation and response serialization:
- `UserCreate`: Input for creating users
- `UserUpdate`: Input for updating users
- `UserResponse`: Output for user data

### Database Layer (`database/`)

#### Base Configuration (`base.py`)

SQLAlchemy async engine and session management:

```python
from src.infrastructure.database.base import get_session

@router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    ...
```

#### SQL Repositories (`sql/repositories/`)

Implementations of repository ports using SQLAlchemy:

```python
from src.infrastructure.database.sql.repositories.user_repository import SQLUserRepository

repository = SQLUserRepository(session)
user = await repository.get_by_id(1)
```

### External Services (`external/`)

Adapters for third-party services like Amazon Bedrock for AI/ML capabilities.

## Usage Examples

### Creating a User via API

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/users",
        json={"email": "user@example.com", "name": "John Doe"}
    )
    user = response.json()
```

### Using Repository Directly

```python
from src.infrastructure.database.sql.repositories.user_repository import SQLUserRepository
from src.infrastructure.database.base import get_session

async for session in get_session():
    repository = SQLUserRepository(session)
    users = await repository.list_all(skip=0, limit=10)
```

## Testing

Run infrastructure tests:

```bash
# Unit tests
pytest tests/unit/infrastructure/ -v

# Integration tests (requires database)
pytest tests/integration/infrastructure/ -v
```

## Error Handling

The API layer handles domain exceptions and converts them to HTTP responses:

| Domain Exception | HTTP Status | Description |
|-----------------|-------------|-------------|
| `InvalidEmailError` | 400 | Invalid email format |
| `InvalidNameError` | 400 | Name validation failed |
| `UserNotFoundError` | 404 | User not found |
| `EmailAlreadyExistsError` | 409 | Email already registered |

## Changelog

- Initial implementation with User CRUD operations
- JWT authentication support
- SQLAlchemy async repository implementation
