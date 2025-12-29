"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.models.user import User


def test_login_success(client: TestClient, test_user: User):
    """Test successful login."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.username,
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_email(client: TestClient, test_user: User):
    """Test login with email instead of username."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client: TestClient, test_user: User):
    """Test login with wrong password."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user.username,
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient):
    """Test login with non-existent user."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "nonexistent",
            "password": "password123",
        },
    )
    assert response.status_code == 401


def test_get_current_user(
    client: TestClient, user_token_headers: dict, test_user: User
):
    """Test getting current user info."""
    response = client.get("/api/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username
    assert "hashed_password" not in data


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without authentication."""
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token(client: TestClient):
    """Test getting current user with invalid token."""
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
