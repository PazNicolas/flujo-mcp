"""Tests for item endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.models.user import User


def test_create_item(client: TestClient, user_token_headers: dict):
    """Test creating an item."""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item",
    }
    response = client.post(
        "/api/items/", json=item_data, headers=user_token_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    assert "owner_id" in data


def test_create_item_unauthorized(client: TestClient):
    """Test creating item without authentication."""
    item_data = {
        "title": "Test Item",
        "description": "This should fail",
    }
    response = client.post("/api/items/", json=item_data)
    assert response.status_code == 401


def test_read_items(client: TestClient, user_token_headers: dict):
    """Test reading user's items."""
    # Create an item first
    item_data = {"title": "Test Item", "description": "Description"}
    client.post("/api/items/", json=item_data, headers=user_token_headers)

    # Read items
    response = client.get("/api/items/", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_item_by_id(client: TestClient, user_token_headers: dict):
    """Test reading specific item by ID."""
    # Create an item
    item_data = {"title": "Specific Item", "description": "Description"}
    create_response = client.post(
        "/api/items/", json=item_data, headers=user_token_headers
    )
    item_id = create_response.json()["id"]

    # Read the item
    response = client.get(
        f"/api/items/{item_id}", headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]


def test_read_item_not_found(client: TestClient, user_token_headers: dict):
    """Test reading non-existent item."""
    response = client.get("/api/items/99999", headers=user_token_headers)
    assert response.status_code == 404


def test_update_item(client: TestClient, user_token_headers: dict):
    """Test updating an item."""
    # Create an item
    item_data = {"title": "Original Title", "description": "Original"}
    create_response = client.post(
        "/api/items/", json=item_data, headers=user_token_headers
    )
    item_id = create_response.json()["id"]

    # Update the item
    update_data = {"title": "Updated Title"}
    response = client.patch(
        f"/api/items/{item_id}", json=update_data, headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == "Original"  # Should remain unchanged


def test_delete_item(client: TestClient, user_token_headers: dict):
    """Test deleting an item."""
    # Create an item
    item_data = {"title": "To Delete", "description": "Will be deleted"}
    create_response = client.post(
        "/api/items/", json=item_data, headers=user_token_headers
    )
    item_id = create_response.json()["id"]

    # Delete the item
    response = client.delete(
        f"/api/items/{item_id}", headers=user_token_headers
    )
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(
        f"/api/items/{item_id}", headers=user_token_headers
    )
    assert get_response.status_code == 404


def test_user_cannot_access_other_user_items(
    client: TestClient, user_token_headers: dict, superuser_token_headers: dict
):
    """Test that users cannot access items from other users."""
    # Create item as superuser
    item_data = {"title": "Superuser Item", "description": "Private"}
    create_response = client.post(
        "/api/items/", json=item_data, headers=superuser_token_headers
    )
    item_id = create_response.json()["id"]

    # Try to access as normal user
    response = client.get(
        f"/api/items/{item_id}", headers=user_token_headers
    )
    assert response.status_code == 403
