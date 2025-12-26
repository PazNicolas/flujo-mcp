from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency to get database session.

    Yields:
        Database session that auto-commits on success or rollbacks on error
    """
    with Session(engine) as session:
        yield session
