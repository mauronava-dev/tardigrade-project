# Module Documentation Guidelines

## Requirement

Every module directory must contain a `README.md` file to facilitate team onboarding.

## README.md Structure

```markdown
# Module Name

## Description
Brief description of the module's purpose and responsibility.

## Business Rules
- Rule 1: Description of business rule
- Rule 2: Description of business rule

## Dependencies
- Internal: List of internal modules this depends on
- External: List of external packages used

## Directory Structure
```
module/
├── file1.py    # Description
└── file2.py    # Description
```

## Usage Examples
Code examples showing how to use this module.

## Testing
How to run tests for this module.

## Changelog
Notable changes to this module.
```

## Example: Domain Entity README

```markdown
# Users Domain

## Description
Handles user-related business logic and entities.

## Business Rules
- Email must be unique across all users
- Password must be at least 8 characters
- Users cannot delete their own account
- Inactive users cannot authenticate

## Dependencies
- Internal: None (domain has no internal dependencies)
- External: None (pure Python)

## Entities
- `User`: Core user entity with validation
- `UserRole`: Enum of available roles

## Usage
```python
from domain.entities.user import User

user = User(email="test@example.com", name="John")
```
```

## When to Update README

- Adding new business rules
- Adding new public functions/classes
- Changing module dependencies
- Breaking changes to interfaces
