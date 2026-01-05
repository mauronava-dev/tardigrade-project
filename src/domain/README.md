# Domain Layer

## Description

The domain layer contains the core business logic and entities of the Tardigrade application. This layer has no external dependencies and represents the heart of the hexagonal architecture.

## Business Rules

- Email must be unique across all users
- Email must contain an "@" character to be valid
- User name must be at least 2 characters long
- Users can be active or inactive
- Domain exceptions are raised for business rule violations

## Dependencies

- Internal: None (domain has no internal dependencies)
- External: None (pure Python)

## Directory Structure

```
domain/
├── __init__.py
├── README.md
├── entities/
│   ├── __init__.py
│   └── user.py           # User domain entity with validation
├── services/
│   └── __init__.py       # Domain services (business logic)
├── prompts/
│   └── __init__.py       # Prompt templates for AI agents
└── exceptions/
    ├── __init__.py
    └── domain_exceptions.py  # Domain-specific exceptions
```

## Entities

### User

Core user entity with validation logic.

```python
from src.domain.entities import User

user = User(
    id=None,
    email="user@example.com",
    name="John Doe",
    is_active=True
)
user.validate()  # Raises InvalidEmailError or InvalidNameError if invalid
```

## Exceptions

| Exception | Description |
|-----------|-------------|
| `DomainError` | Base exception for all domain errors |
| `InvalidEmailError` | Raised when email format is invalid |
| `InvalidNameError` | Raised when name is too short |
| `UserNotFoundError` | Raised when user is not found |
| `EmailAlreadyExistsError` | Raised when email already exists |

## Usage Examples

### Creating and Validating a User

```python
from src.domain.entities import User
from src.domain.exceptions import InvalidEmailError, InvalidNameError

# Create a valid user
user = User(id=None, email="test@example.com", name="John Doe")
user.validate()  # No exception raised

# Invalid email raises exception
try:
    invalid_user = User(id=None, email="invalid-email", name="John")
    invalid_user.validate()
except InvalidEmailError as e:
    print(f"Invalid email: {e.email}")

# Short name raises exception
try:
    short_name_user = User(id=None, email="test@example.com", name="J")
    short_name_user.validate()
except InvalidNameError as e:
    print(f"Invalid name: {e.name}")
```

## Testing

Run domain layer tests:

```bash
pytest tests/unit/domain/ -v
```

## Changelog

- Initial implementation with User entity and domain exceptions
