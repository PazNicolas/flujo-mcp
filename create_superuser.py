"""Script para crear un superusuario."""

from sqlmodel import Session
from app.core.database import engine
from app.core.security import get_password_hash
from app.models.user import User


def create_superuser(
    email: str = "admin@example.com",
    username: str = "admin",
    password: str = "admin123",
    full_name: str = "Administrator",
) -> None:
    """Create a superuser in the database."""
    with Session(engine) as session:
        # Check if user already exists
        existing = (
            session.query(User)
            .filter((User.email == email) | (User.username == username))
            .first()
        )

        if existing:
            print(f"User with email '{email}' or username '{username}' already exists!")
            return

        superuser = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            is_superuser=True,
        )
        session.add(superuser)
        session.commit()
        print(f"Superuser '{username}' created successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        create_superuser(
            email=sys.argv[1],
            username=sys.argv[2],
            password=sys.argv[3],
            full_name=sys.argv[4] if len(sys.argv) > 4 else "Administrator",
        )
    else:
        print(
            "Usage: python create_superuser.py <email> <username> <password> [full_name]"
        )
        print("\nUsing default values...")
        create_superuser()
