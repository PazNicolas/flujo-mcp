from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth, users
from app.core.config import settings
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Create database tables if they don't exist
    # Note: In production, use Alembic migrations instead
    # create_db_and_tables()
    yield
    # Shutdown: cleanup code here if needed


app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI application with SQLModel, Alembic and JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Flujo-MCP API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
