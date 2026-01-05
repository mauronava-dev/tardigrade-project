"""Domain exceptions module."""

from src.domain.exceptions.domain_exceptions import (
    DomainError,
    EmailAlreadyExistsError,
    InvalidEmailError,
    InvalidNameError,
    UserNotFoundError,
)

__all__ = [
    "DomainError",
    "InvalidEmailError",
    "InvalidNameError",
    "UserNotFoundError",
    "EmailAlreadyExistsError",
]
