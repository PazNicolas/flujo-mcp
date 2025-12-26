from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.user import User, UserCreate, UserPublic, UserUpdate
from app.api.deps import CurrentUser, CurrentSuperUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    session: Annotated[Session, Depends(get_session)],
    user_in: UserCreate,
) -> User:
    """
    Create a new user (public registration).
    """
    # Check if email already exists
    existing_email = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username already exists
    existing_username = session.exec(
        select(User).where(User.username == user_in.username)
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create new user with hashed password
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=list[UserPublic])
def read_users(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentSuperUser,  # Only superusers can list all users
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[User]:
    """
    Get all users (superuser only).
    """
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> User:
    """
    Get current user.
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentUser,
    user_in: UserUpdate,
) -> User:
    """
    Update current user.
    """
    # Check if email is being changed and if it already exists
    if user_in.email and user_in.email != current_user.email:
        existing_email = session.exec(
            select(User).where(User.email == user_in.email)
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Check if username is being changed and if it already exists
    if user_in.username and user_in.username != current_user.username:
        existing_username = session.exec(
            select(User).where(User.username == user_in.username)
        ).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

    # Update user fields
    user_data = user_in.model_dump(exclude_unset=True)

    # Handle password hashing if password is being updated
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

    user_data["updated_at"] = datetime.utcnow()

    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.get("/{user_id}", response_model=UserPublic)
def read_user(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentSuperUser,  # Only superusers can view other users
    user_id: int,
) -> User:
    """
    Get a specific user by ID (superuser only).
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentSuperUser,  # Only superusers can update other users
    user_id: int,
    user_in: UserUpdate,
) -> User:
    """
    Update a user (superuser only).
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if email is being changed and if it already exists
    if user_in.email and user_in.email != db_user.email:
        existing_email = session.exec(
            select(User).where(User.email == user_in.email)
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Check if username is being changed and if it already exists
    if user_in.username and user_in.username != db_user.username:
        existing_username = session.exec(
            select(User).where(User.username == user_in.username)
        ).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

    # Update user fields
    user_data = user_in.model_dump(exclude_unset=True)

    # Handle password hashing if password is being updated
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

    user_data["updated_at"] = datetime.utcnow()

    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: CurrentSuperUser,  # Only superusers can delete users
    user_id: int,
) -> None:
    """
    Delete a user (superuser only).
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Prevent self-deletion
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete yourself"
        )

    session.delete(user)
    session.commit()
