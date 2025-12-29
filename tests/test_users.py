"""Tests for user endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.models.user import User


def test_create_user(client: TestClient):
    """Test user registration."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword123",
        "full_name": "New User",
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "hashed_password" not in data
    assert "password" not in data


def test_create_user_duplicate_email(client: TestClient, test_user: User):
    """Test creating user with duplicate email."""
    user_data = {
        "email": test_user.email,
        "username": "different_username",
        "password": "password123",
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_create_user_duplicate_username(client: TestClient, test_user: User):
    """Test creating user with duplicate username."""
    user_data = {
        "email": "different@example.com",
        "username": test_user.username,
        "password": "password123",
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_read_users_as_superuser(
    client: TestClient, superuser_token_headers: dict, test_user: User
):
    """Test listing all users as superuser."""
    response = client.get("/api/users/", headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_users_as_normal_user(
    client: TestClient, user_token_headers: dict
):
    """Test that normal users cannot list all users."""
    response = client.get("/api/users/", headers=user_token_headers)
    assert response.status_code == 403


def test_read_user_me(
    client: TestClient, user_token_headers: dict, test_user: User
):
    """Test reading current user info."""
    response = client.get("/api/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username
