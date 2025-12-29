"""Pytest configuration and fixtures for testing."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.user import User


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with test database."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
        is_superuser=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_superuser")
def test_superuser_fixture(session: Session):
    """Create a test superuser."""
    superuser = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpassword123"),
        is_active=True,
        is_superuser=True,
    )
    session.add(superuser)
    session.commit()
    session.refresh(superuser)
    return superuser


@pytest.fixture(name="user_token_headers")
def user_token_headers_fixture(client: TestClient, test_user: User):
    """Get authentication headers for test user."""
    login_data = {
        "username": test_user.username,
        "password": "testpassword123",
    }
    response = client.post("/api/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture(name="superuser_token_headers")
def superuser_token_headers_fixture(client: TestClient, test_superuser: User):
    """Get authentication headers for test superuser."""
    login_data = {
        "username": test_superuser.username,
        "password": "adminpassword123",
    }
    response = client.post("/api/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
