"""User domain entity.

This module contains the User entity which represents a user in the domain layer.
"""

from dataclasses import dataclass
from datetime import datetime

from src.domain.exceptions import InvalidEmailError, InvalidNameError


@dataclass
class User:
    """User domain entity.

    Represents a user in the system with validation logic.

    Attributes:
        id: Unique identifier for the user. None for new users.
        email: User's email address.
        name: User's display name.
        is_active: Whether the user account is active.
        created_at: Timestamp when the user was created.
    """

    id: int | None
    email: str
    name: str
    is_active: bool = True
    created_at: datetime | None = None

    def validate(self) -> None:
        """Validate user data.

        Raises:
            InvalidEmailError: If email format is invalid.
            InvalidNameError: If name is too short.
        """
        if not self.email or "@" not in self.email:
            raise InvalidEmailError(self.email)
        if not self.name or len(self.name) < 2:
            raise InvalidNameError(self.name)
