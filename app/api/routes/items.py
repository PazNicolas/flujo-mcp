from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.item import Item, ItemCreate, ItemPublic, ItemUpdate
from app.api.deps import CurrentUser

router = APIRouter(prefix="/items", tags=["Items"])


@router.post(
    "/", response_model=ItemPublic, status_code=status.HTTP_201_CREATED
)
def create_item(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
    item_in: ItemCreate,
) -> Item:
    """
    Create a new item for the current user.
    """
    db_item = Item(
        title=item_in.title,
        description=item_in.description,
        owner_id=current_user.id,
    )

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.get("/", response_model=list[ItemPublic])
def read_items(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[Item]:
    """
    Get all items for the current user.
    """
    statement = (
        select(Item)
        .where(Item.owner_id == current_user.id)
        .offset(offset)
        .limit(limit)
    )
    items = session.exec(statement).all()
    return list(items)


@router.get("/{item_id}", response_model=ItemPublic)
def read_item(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
    item_id: int,
) -> Item:
    """
    Get a specific item by ID.
    """
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    # Check if the item belongs to the current user
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this item",
        )

    return item


@router.patch("/{item_id}", response_model=ItemPublic)
def update_item(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
    item_id: int,
    item_in: ItemUpdate,
) -> Item:
    """
    Update an item.
    """
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    # Check if the item belongs to the current user
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this item",
        )

    # Update only provided fields
    item_data = item_in.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(item, key, value)

    # Update the updated_at timestamp
    item.updated_at = datetime.utcnow()

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
    item_id: int,
) -> None:
    """
    Delete an item.
    """
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    # Check if the item belongs to the current user
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this item",
        )

    session.delete(item)
    session.commit()
