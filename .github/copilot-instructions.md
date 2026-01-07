# Copilot Instructions - Flujo MCP

## Project Context
FastAPI application demonstrating agentic programming with Model Context Protocol (MCP). Stack: FastAPI + SQLModel + PostgreSQL + JWT auth + Argon2id hashing.

## Architecture

### Core Dependencies Flow
```
Request → OAuth2PasswordBearer → get_current_user → CurrentUser
                                      ↓
                              Session (SessionDep)
                                      ↓
                              PostgreSQL (SQLModel)
```

**Key Type Aliases** (in [app/api/deps.py](app/api/deps.py)):
- `SessionDep`: Database session injection
- `CurrentUser`: Authenticated user from JWT
- `TokenDep`: Bearer token extraction

### Security Layer
- **Passwords**: Argon2id via `argon2-cffi` (never use bcrypt/pbkdf2)
- **JWT**: HS256 with JTI for blacklist support (Redis)
- **Rate Limiting**: 5 failed logins → 5-minute block (Redis-backed)
- **Token Revocation**: Logout adds JTI to Redis blacklist

## Critical Patterns

### 1. Router Structure
Every route file follows this pattern:
```python
from fastapi import APIRouter
from app.api.deps import SessionDep, CurrentUser

router = APIRouter(prefix="/resource", tags=["Resource"])

@router.get("/", response_model=list[ResourceRead])
def list_resources(session: SessionDep, current_user: CurrentUser):
    """List resources. Always include user context."""
```

### 2. Password Operations
**ALWAYS** use these exact functions from [app/core/security.py](app/core/security.py):
```python
from app.core.security import get_password_hash, verify_password

# Hash (registration/password change)
hashed = get_password_hash(plain_password)

# Verify (login)
is_valid = verify_password(plain_password, user.hashed_password)
```

### 3. Database Models vs Schemas
- **Models** ([app/models/](app/models/)): SQLModel with `table=True` for DB tables
- **Schemas** ([app/schemas/](app/schemas/)): Pydantic for API request/response
- Always separate: `UserCreate` (schema) → `User` (model) → `UserRead` (schema)

### 4. Migrations Workflow
```bash
# ALWAYS create migration after model changes
alembic revision --autogenerate -m "add users table"
# Review generated file in alembic/versions/
alembic upgrade head
```
Never use `SQLModel.metadata.create_all()` in production code.

## Quick Start Commands

### Development
```bash
make deps-up          # Start PostgreSQL + Redis + pgAdmin
make install          # Install Python deps
make db-upgrade       # Apply migrations
make dev              # Run server (localhost:8000)
python create_superuser.py  # Create admin
```

### Testing
```bash
pytest                           # Run all tests
pytest tests/test_auth.py -v    # Specific test with verbose
pytest --cov=app                # With coverage
```

## Common Tasks

### Add New Endpoint
1. Create route in `app/api/routes/resource.py`
2. Import and include router in [app/main.py](app/main.py): `app.include_router(resource.router, prefix="/api")`
3. Use `SessionDep` for DB, `CurrentUser` for auth
4. Document with docstrings (shown in `/docs`)

### Add Database Table
1. Create model in `app/models/resource.py` with `table=True`
2. Create schemas in `app/schemas/resource.py` (Read/Create/Update)
3. Generate migration: `alembic revision --autogenerate -m "add resource"`
4. Review and apply: `alembic upgrade head`

### Protect Endpoints
```python
from app.api.deps import CurrentUser

@router.get("/protected")
def protected_route(current_user: CurrentUser):
    # Current user auto-injected, 401 if invalid token
    return {"user": current_user.email}
```

## Context7 Library IDs
**Always consult these BEFORE implementing** (use MCP):
- FastAPI: `/fastapi/fastapi`
- SQLModel: `/websites/sqlmodel_tiangolo`
- Alembic: `/sqlalchemy/alembic`
- Argon2: `/hynek/argon2-cffi`

## Error Patterns

### Authentication Errors
```python
# Use exact status codes from examples
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},  # Required for OAuth2
)
```

### Not Found
```python
if not resource:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Resource {id} not found"
    )
```

## Testing Strategy
**Fixtures** (in [tests/conftest.py](tests/conftest.py)):
- `session`: In-memory SQLite database
- `client`: TestClient with overridden dependencies
- `test_user`: Pre-created user for auth tests

**Pattern**:
```python
def test_endpoint(client, test_user):
    # Login to get token
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Use token in protected endpoint
    response = client.get("/api/protected", 
        headers={"Authorization": f"Bearer {token}"})
```

## What NOT to Do
- ❌ Don't use bcrypt/sha256 for passwords (use Argon2id only)
- ❌ Don't commit `.env` file (use `.env.example` as template)
- ❌ Don't create tables with `create_all()` (use Alembic)
- ❌ Don't put database logic in routes (keep routes thin)
- ❌ Don't hardcode `SECRET_KEY` (always from `settings`)

## Related Documentation
- Full conventions: [.github/instructions.md](.github/instructions.md)
- MCP workflow: [.github/agents/MCP-Notion.agent.md](.github/agents/MCP-Notion.agent.md)
- Quick start: [README.md](../README.md)
