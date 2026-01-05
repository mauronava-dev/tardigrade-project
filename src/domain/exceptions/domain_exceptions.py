"""Domain exceptions for the Tardigrade project.

This module contains all domain-specific exceptions that represent
business rule violations and domain errors.
"""


class DomainError(Exception):
    """Base domain exception.

    All domain-specific exceptions should inherit from this class.
    """

    def __init__(self, message: str = "A domain error occurred"):
        self.message = message
        super().__init__(self.message)


class InvalidEmailError(DomainError):
    """Raised when email format is invalid.

    Args:
        email: The invalid email address.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Invalid email format: {email}")


class InvalidNameError(DomainError):
    """Raised when name does not meet requirements.

    Args:
        name: The invalid name.
    """

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Invalid name: {name}. Name must be at least 2 characters.")


class UserNotFoundError(DomainError):
    """Raised when a user is not found.

    Args:
        user_id: The ID of the user that was not found.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User not found with ID: {user_id}")


class EmailAlreadyExistsError(DomainError):
    """Raised when attempting to create a user with an existing email.

    Args:
        email: The email address that already exists.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email already exists: {email}")
