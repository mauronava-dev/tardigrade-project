"""User test data factory.

This module provides factory classes for generating User test data
using factory_boy library.
"""

from datetime import datetime, timezone

import factory

from src.domain.entities.user import User


class UserFactory(factory.Factory):
    """Factory for creating User domain entities.

    Usage:
        # Create a user with default values
        user = UserFactory.build()

        # Create a user with custom values
        user = UserFactory.build(email="custom@example.com")

        # Create multiple users
        users = UserFactory.build_batch(5)

        # Create a user with a specific ID
        user = UserFactory.build(id=42)
    """

    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyAttribute(lambda obj: f"user{obj.id}@example.com")
    name = factory.Faker("name")
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive User entities."""

    is_active = False


class UserCreateDataFactory(factory.DictFactory):
    """Factory for creating user creation request data.

    Usage:
        # Create request data with default values
        data = UserCreateDataFactory.build()

        # Create request data with custom email
        data = UserCreateDataFactory.build(email="custom@example.com")
    """

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")


class InvalidUserFactory(factory.Factory):
    """Factory for creating invalid User entities for testing validation.

    Usage:
        # Create user with invalid email
        user = InvalidUserFactory.build(email="invalid-email")

        # Create user with short name
        user = InvalidUserFactory.build(name="A")
    """

    class Meta:
        model = User

    id = None
    email = "invalid-email"  # Missing @ symbol
    name = "A"  # Too short
    is_active = True
    created_at = None
