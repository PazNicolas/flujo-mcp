from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class ItemBase(SQLModel):
    """Base item model with shared attributes."""

    title: str = Field(min_length=1, max_length=255, index=True)
    description: str | None = Field(default=None, max_length=1000)


class Item(ItemBase, table=True):
    """Item database model."""

    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int | None = Field(
        default=None, foreign_key="users.id", index=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User model
    owner: Optional["User"] = Relationship()


class ItemCreate(SQLModel):
    """Schema for creating a new item."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class ItemUpdate(SQLModel):
    """Schema for updating an item."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class ItemPublic(ItemBase):
    """Schema for public item data."""

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
