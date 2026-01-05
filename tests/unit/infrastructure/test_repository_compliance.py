"""Property-based tests for repository port compliance.

Feature: project-initialization, Property 3: Repository Port Compliance
Validates: Requirements 4.9
"""

import inspect
from abc import abstractmethod

import pytest
from hypothesis import given, settings, strategies as st

from src.application.interfaces.repository_port import UserRepositoryPort
from src.infrastructure.database.sql.repositories.user_repository import SQLUserRepository


# Feature: project-initialization, Property 3: Repository Port Compliance
# For any repository implementation (SQLUserRepository), it SHALL implement
# all abstract methods defined in UserRepositoryPort without raising NotImplementedError.


def get_abstract_methods(cls: type) -> set[str]:
    """Get all abstract method names from a class.

    Args:
        cls: The class to inspect.

    Returns:
        Set of abstract method names.
    """
    abstract_methods = set()
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if getattr(method, "__isabstractmethod__", False):
            abstract_methods.add(name)
    return abstract_methods


def get_implemented_methods(cls: type) -> set[str]:
    """Get all method names implemented by a class.

    Args:
        cls: The class to inspect.

    Returns:
        Set of implemented method names.
    """
    implemented = set()
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Check if method is defined in the class itself (not inherited abstract)
        if name in cls.__dict__ or not getattr(method, "__isabstractmethod__", False):
            implemented.add(name)
    return implemented


@settings(max_examples=100)
@given(method_index=st.integers(min_value=0, max_value=100))
def test_sql_repository_implements_all_port_methods(method_index: int) -> None:
    """For any abstract method in UserRepositoryPort, SQLUserRepository SHALL implement it.

    Feature: project-initialization, Property 3: Repository Port Compliance
    Validates: Requirements 4.9

    This property test verifies that for any randomly selected abstract method
    from the port interface, the repository implementation provides a concrete
    implementation.
    """
    # Get abstract methods from the port
    abstract_methods = get_abstract_methods(UserRepositoryPort)
    abstract_method_list = sorted(list(abstract_methods))

    # Use modulo to select a method (property-based approach)
    if abstract_method_list:
        selected_index = method_index % len(abstract_method_list)
        method_name = abstract_method_list[selected_index]

        # Verify the method exists in SQLUserRepository
        assert hasattr(SQLUserRepository, method_name), (
            f"SQLUserRepository missing method: {method_name}"
        )

        # Verify the method is not abstract (i.e., it's implemented)
        impl_method = getattr(SQLUserRepository, method_name)
        assert not getattr(impl_method, "__isabstractmethod__", False), (
            f"Method {method_name} is still abstract in SQLUserRepository"
        )


def test_sql_repository_is_subclass_of_port() -> None:
    """SQLUserRepository SHALL be a subclass of UserRepositoryPort.

    Feature: project-initialization, Property 3: Repository Port Compliance
    Validates: Requirements 4.9
    """
    assert issubclass(SQLUserRepository, UserRepositoryPort), (
        "SQLUserRepository must inherit from UserRepositoryPort"
    )


def test_all_abstract_methods_implemented() -> None:
    """All abstract methods from UserRepositoryPort SHALL be implemented.

    Feature: project-initialization, Property 3: Repository Port Compliance
    Validates: Requirements 4.9
    """
    abstract_methods = get_abstract_methods(UserRepositoryPort)

    for method_name in abstract_methods:
        # Check method exists
        assert hasattr(SQLUserRepository, method_name), (
            f"SQLUserRepository missing method: {method_name}"
        )

        # Check method is not abstract
        impl_method = getattr(SQLUserRepository, method_name)
        assert not getattr(impl_method, "__isabstractmethod__", False), (
            f"Method {method_name} is still abstract in SQLUserRepository"
        )


def test_method_signatures_match() -> None:
    """Method signatures in SQLUserRepository SHALL match UserRepositoryPort.

    Feature: project-initialization, Property 3: Repository Port Compliance
    Validates: Requirements 4.9
    """
    abstract_methods = get_abstract_methods(UserRepositoryPort)

    for method_name in abstract_methods:
        port_method = getattr(UserRepositoryPort, method_name)
        impl_method = getattr(SQLUserRepository, method_name)

        port_sig = inspect.signature(port_method)
        impl_sig = inspect.signature(impl_method)

        # Compare parameter names (excluding 'self')
        port_params = [p for p in port_sig.parameters.keys() if p != "self"]
        impl_params = [p for p in impl_sig.parameters.keys() if p != "self"]

        assert port_params == impl_params, (
            f"Method {method_name} signature mismatch: "
            f"port has {port_params}, impl has {impl_params}"
        )
