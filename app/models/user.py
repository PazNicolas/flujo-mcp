from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base user model with shared attributes."""

    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    """User database model."""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(SQLModel):
    """Schema for creating a new user."""

    email: str = Field(max_length=255)
    username: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(SQLModel):
    """Schema for updating a user."""

    email: str | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=100)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class UserPublic(UserBase):
    """Schema for public user data (without password)."""

    id: int
    created_at: datetime
    updated_at: datetime
