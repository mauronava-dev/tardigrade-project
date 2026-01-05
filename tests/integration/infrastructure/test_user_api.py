"""Integration tests for User API endpoints.

These tests verify the complete request/response cycle for user CRUD operations.
Validates: Requirements 10.7
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUserAPI:
    """Integration tests for User API endpoints."""

    async def test_create_user_success(self, client: AsyncClient) -> None:
        """Test successful user creation."""
        response = await client.post(
            "/api/v1/users/",
            json={"email": "test@example.com", "name": "Test User"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    async def test_create_user_invalid_email(self, client: AsyncClient) -> None:
        """Test user creation with invalid email returns 400."""
        response = await client.post(
            "/api/v1/users/",
            json={"email": "invalid-email", "name": "Test User"},
        )

        assert response.status_code == 400
        assert "Invalid email" in response.json()["detail"]

    async def test_create_user_short_name(self, client: AsyncClient) -> None:
        """Test user creation with short name returns 400."""
        response = await client.post(
            "/api/v1/users/",
            json={"email": "test@example.com", "name": "A"},
        )

        assert response.status_code == 422  # Pydantic validation

    async def test_create_user_duplicate_email(self, client: AsyncClient) -> None:
        """Test user creation with duplicate email returns 409."""
        # Create first user
        await client.post(
            "/api/v1/users/",
            json={"email": "duplicate@example.com", "name": "First User"},
        )

        # Try to create second user with same email
        response = await client.post(
            "/api/v1/users/",
            json={"email": "duplicate@example.com", "name": "Second User"},
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    async def test_get_user_success(self, client: AsyncClient) -> None:
        """Test getting a user by ID."""
        # Create a user first
        create_response = await client.post(
            "/api/v1/users/",
            json={"email": "getuser@example.com", "name": "Get User"},
        )
        user_id = create_response.json()["id"]

        # Get the user
        response = await client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "getuser@example.com"
        assert data["name"] == "Get User"

    async def test_get_user_not_found(self, client: AsyncClient) -> None:
        """Test getting a non-existent user returns 404."""
        response = await client.get("/api/v1/users/99999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_list_users_empty(self, client: AsyncClient) -> None:
        """Test listing users when none exist."""
        response = await client.get("/api/v1/users/")

        assert response.status_code == 200
        assert response.json() == []

    async def test_list_users_with_data(self, client: AsyncClient) -> None:
        """Test listing users returns created users."""
        # Create users
        await client.post(
            "/api/v1/users/",
            json={"email": "user1@example.com", "name": "User One"},
        )
        await client.post(
            "/api/v1/users/",
            json={"email": "user2@example.com", "name": "User Two"},
        )

        # List users
        response = await client.get("/api/v1/users/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        emails = [user["email"] for user in data]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails

    async def test_list_users_pagination(self, client: AsyncClient) -> None:
        """Test listing users with pagination."""
        # Create 3 users
        for i in range(3):
            await client.post(
                "/api/v1/users/",
                json={"email": f"page{i}@example.com", "name": f"Page User {i}"},
            )

        # Get first page
        response = await client.get("/api/v1/users/?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Get second page
        response = await client.get("/api/v1/users/?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_update_user_success(self, client: AsyncClient) -> None:
        """Test updating a user."""
        # Create a user
        create_response = await client.post(
            "/api/v1/users/",
            json={"email": "update@example.com", "name": "Original Name"},
        )
        user_id = create_response.json()["id"]

        # Update the user
        response = await client.put(
            f"/api/v1/users/{user_id}",
            json={"name": "Updated Name"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "update@example.com"

    async def test_update_user_not_found(self, client: AsyncClient) -> None:
        """Test updating a non-existent user returns 404."""
        response = await client.put(
            "/api/v1/users/99999",
            json={"name": "New Name"},
        )

        assert response.status_code == 404

    async def test_delete_user_success(self, client: AsyncClient) -> None:
        """Test deleting a user."""
        # Create a user
        create_response = await client.post(
            "/api/v1/users/",
            json={"email": "delete@example.com", "name": "Delete User"},
        )
        user_id = create_response.json()["id"]

        # Delete the user
        response = await client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == 204

        # Verify user is deleted
        get_response = await client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 404

    async def test_delete_user_not_found(self, client: AsyncClient) -> None:
        """Test deleting a non-existent user returns 404."""
        response = await client.delete("/api/v1/users/99999")

        assert response.status_code == 404


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Integration tests for health and root endpoints."""

    async def test_health_check(self, client: AsyncClient) -> None:
        """Test health check endpoint."""
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    async def test_root_endpoint(self, client: AsyncClient) -> None:
        """Test root endpoint."""
        response = await client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "version" in data
