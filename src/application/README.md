# Application Layer

## Description

The application layer orchestrates business operations by coordinating between domain entities and infrastructure adapters. It contains use cases that implement application-specific business rules and port definitions (interfaces) that abstract external dependencies.

## Business Rules

- Use cases validate domain entities before persistence
- Email uniqueness is enforced at the application layer
- Users must exist before they can be retrieved or deleted
- Pagination is supported for listing operations

## Dependencies

- Internal: `src.domain` (entities, exceptions)
- External: None (ports are abstract interfaces)

## Directory Structure

```
application/
├── __init__.py           # Package initialization
├── README.md             # This documentation
├── interfaces/           # Port definitions (abstract interfaces)
│   ├── __init__.py
│   ├── repository_port.py  # User repository interface
│   └── llm_port.py         # LLM interaction interface
└── use_cases/            # Application use cases
    ├── __init__.py
    └── user_use_cases.py   # User CRUD operations
```

## Ports (Interfaces)

### UserRepositoryPort

Abstract interface for user persistence operations:

- `get_by_id(user_id)` - Retrieve user by ID
- `get_by_email(email)` - Retrieve user by email
- `save(user)` - Create or update user
- `delete(user_id)` - Delete user
- `list_all(skip, limit)` - List users with pagination

### LLMPort

Abstract interface for LLM interactions:

- `invoke(prompt, user_input)` - Single LLM invocation
- `invoke_with_history(prompt, messages, user_input)` - Conversational LLM

## Use Cases

### CreateUserUseCase

Creates a new user after validating data and checking email uniqueness.

```python
from src.application.use_cases import CreateUserUseCase

use_case = CreateUserUseCase(repository)
user = await use_case.execute(email="user@example.com", name="John Doe")
```

### GetUserUseCase

Retrieves a user by their unique identifier.

```python
from src.application.use_cases import GetUserUseCase

use_case = GetUserUseCase(repository)
user = await use_case.execute(user_id=1)
```

### ListUsersUseCase

Lists users with pagination support.

```python
from src.application.use_cases import ListUsersUseCase

use_case = ListUsersUseCase(repository)
users = await use_case.execute(skip=0, limit=10)
```

### DeleteUserUseCase

Deletes a user by their unique identifier.

```python
from src.application.use_cases import DeleteUserUseCase

use_case = DeleteUserUseCase(repository)
deleted = await use_case.execute(user_id=1)
```

## Testing

Run application layer tests:

```bash
pytest tests/unit/application/ -v
```

## Changelog

- Initial implementation with User CRUD use cases
- Added UserRepositoryPort and LLMPort interfaces
