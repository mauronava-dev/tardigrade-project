"""Property-based tests for User entity validation.

Feature: project-initialization, Property 1: User Entity Validation
Validates: Requirements 2.5
"""

import pytest
from hypothesis import given, settings, strategies as st

from src.domain.entities.user import User
from src.domain.exceptions import InvalidEmailError, InvalidNameError


# Feature: project-initialization, Property 1: User Entity Validation
# For any User entity with an email that does not contain "@" or a name with
# fewer than 2 characters, calling validate() SHALL raise the appropriate
# domain exception (InvalidEmailError or InvalidNameError).


@settings(max_examples=100)
@given(
    email=st.text().filter(lambda x: "@" not in x),
    name=st.text(min_size=2)
)
def test_invalid_email_raises_error(email: str, name: str) -> None:
    """For any email without @, validation should raise InvalidEmailError.

    Feature: project-initialization, Property 1: User Entity Validation
    Validates: Requirements 2.5
    """
    user = User(id=None, email=email, name=name)
    with pytest.raises(InvalidEmailError):
        user.validate()


@settings(max_examples=100)
@given(
    email=st.emails(),
    name=st.text(max_size=1)
)
def test_short_name_raises_error(email: str, name: str) -> None:
    """For any name with fewer than 2 characters, validation should raise InvalidNameError.

    Feature: project-initialization, Property 1: User Entity Validation
    Validates: Requirements 2.5
    """
    user = User(id=None, email=email, name=name)
    with pytest.raises(InvalidNameError):
        user.validate()


@settings(max_examples=100)
@given(
    email=st.emails(),
    name=st.text(min_size=2, max_size=100).filter(lambda x: len(x.strip()) >= 2)
)
def test_valid_user_passes_validation(email: str, name: str) -> None:
    """For any valid email and name, validation should pass without exception.

    Feature: project-initialization, Property 1: User Entity Validation
    Validates: Requirements 2.5
    """
    user = User(id=None, email=email, name=name)
    # Should not raise any exception
    user.validate()


def test_empty_email_raises_error() -> None:
    """Empty email should raise InvalidEmailError."""
    user = User(id=None, email="", name="John Doe")
    with pytest.raises(InvalidEmailError):
        user.validate()


def test_empty_name_raises_error() -> None:
    """Empty name should raise InvalidNameError."""
    user = User(id=None, email="test@example.com", name="")
    with pytest.raises(InvalidNameError):
        user.validate()
