# Instrucciones del Proyecto - Flujo MCP

> **Lee también**: [MCP-Notion.agent.md](./MCP-Notion.agent.md) - Flujo de trabajo estándar con MCPs (aplica a todos los proyectos de la organización)

---

## 🎯 Propósito del Proyecto

Este proyecto es una aplicación FastAPI que sirve como **banco de pruebas** para flujos de trabajo automatizados usando Model Context Protocol (MCP). El objetivo es demostrar cómo los agentes de IA pueden:

1. Obtener requerimientos desde Notion
2. Implementar código de forma autónoma
3. Crear Pull Requests en GitHub
4. Documentar cambios automáticamente

---

## 🏗️ Stack Tecnológico

### Backend
- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.22+
- **Base de datos**: PostgreSQL con psycopg2-binary
- **Migraciones**: Alembic 1.14+
- **Servidor**: Uvicorn con extras standard

### Seguridad
- **Autenticación**: JWT con PyJWT 2.9+
- **Hashing de contraseñas**: Argon2id via argon2-cffi 23.1+
- **Validación**: Pydantic (incluido en FastAPI)

### Utilidades
- **Settings**: pydantic-settings 2.5+
- **Forms**: python-multipart (para OAuth2PasswordRequestForm)

---

## 📚 Context7 Library IDs del Proyecto

**⚠️ Consulta estas librerías en Context7 ANTES de implementar código:**

| Librería | Context7 ID | Uso |
|----------|-------------|-----|
| FastAPI | `/fastapi/fastapi` | Framework web, routing, validación |
| SQLModel | `/websites/sqlmodel_tiangolo` | ORM, modelos de base de datos |
| Alembic | `/sqlalchemy/alembic` | Migraciones de esquema de BD |
| Argon2 | `/hynek/argon2-cffi` | Hashing seguro de contraseñas |
| Pydantic | `/pydantic/pydantic` | Validación y schemas |
| PyJWT | - | Tokens JWT (consultar docs oficiales) |

---

## � Estructura del Proyecto

```
flujo-mcp/
├── app/
│   ├── api/
│   │   ├── deps.py           # Dependencias compartidas (CurrentUser, etc.)
│   │   └── routes/           # Endpoints de la API
│   │       ├── auth.py       # Login, logout, /me
│   │       ├── items.py      # CRUD de items (ejemplo)
│   │       └── users.py      # CRUD de usuarios
│   ├── core/
│   │   ├── config.py         # Settings con pydantic-settings
│   │   ├── database.py       # Conexión SQLModel/PostgreSQL
│   │   └── security.py       # Argon2, JWT, funciones de auth
│   ├── models/               # Modelos SQLModel (tablas)
│   │   ├── user.py           
│   │   └── item.py
│   ├── schemas/              # Schemas Pydantic (request/response)
│   │   └── token.py
│   └── main.py               # App FastAPI principal
├── alembic/
│   └── versions/             # Migraciones de BD
├── .env                      # Variables de entorno (NO COMMITEAR)
├── alembic.ini              
├── requirements.txt
└── README.md
```

---

## 📝 Convenciones de Código

### Python

#### Estilo General
- **Formateo**: Black (líneas de 88 caracteres)
- **Imports**: Organización con isort
  ```python
  # 1. Standard library
  from datetime import datetime
  from typing import Annotated
  
  # 2. Third-party
  from fastapi import APIRouter, Depends
  from sqlmodel import Session, select
  
  # 3. Local
  from app.core.database import get_session
  from app.models.user import User
  ```
- **Type hints**: Obligatorios en todas las funciones públicas
- **Docstrings**: Google style para funciones y clases complejas

#### Ejemplo de Función
```python
def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: The subject of the token (usually user id or email)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    # Implementation...
```

### FastAPI - Endpoints

#### Estructura de Router
```python
from fastapi import APIRouter

router = APIRouter(prefix="/resource", tags=["Resource"])

@router.get("/", response_model=list[ResourceRead])
def list_resources(session: SessionDep) -> list[Resource]:
    """List all resources."""
    pass

@router.post("/", response_model=ResourceRead, status_code=201)
def create_resource(
    session: SessionDep, 
    resource_in: ResourceCreate
) -> Resource:
    """Create a new resource."""
    pass
```

#### Verbos HTTP
- **GET**: Lectura (no modifica datos)
- **POST**: Creación de recursos
- **PATCH**: Actualización parcial
- **PUT**: Reemplazo completo (usar con precaución)
- **DELETE**: Eliminación

#### Manejo de Errores
```python
from fastapi import HTTPException, status

# 400 - Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 401 - Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# 404 - Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# 409 - Conflict
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Resource already exists"
)
```

### SQLModel - Base de Datos

#### Modelos de Tabla
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    """User database model."""
    __tablename__ = "users"
    
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Schemas de Request/Response
```python
# Separate from table models!
class UserCreate(SQLModel):
    """Schema for creating a user."""
    email: str
    username: str
    password: str

class UserRead(SQLModel):
    """Schema for reading a user (no password!)."""
    id: int
    email: str
    username: str
    is_active: bool
```

#### Migraciones con Alembic

**⚠️ NUNCA modificar la BD directamente - SIEMPRE usar migraciones**

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Add column to users table"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

**Reglas:**
1. Revisar el archivo de migración generado antes de aplicar
2. Probar migraciones en desarrollo antes de producción
3. Nombrar migraciones descriptivamente
4. No editar migraciones ya aplicadas en producción

---

## ⚠️ Reglas Específicas del Proyecto

### Seguridad

#### Autenticación
- **Hashing de passwords**: Usar SOLO Argon2id (ya configurado)
  ```python
  from app.core.security import get_password_hash, verify_password
  
  # Hash al crear usuario
  hashed = get_password_hash(plain_password)
  
  # Verificar en login
  is_valid = verify_password(plain_password, hashed)
  ```

- **JWT Tokens**: Configuración en `.env`
  ```
  SECRET_KEY=your-secret-key-here  # Generar con openssl rand -hex 32
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  ALGORITHM=HS256
  ```

#### Variables Sensibles
**NUNCA commitear:**
- Passwords de BD
- SECRET_KEY de JWT
- API keys externas
- Credenciales de terceros

**Usar `.env` y cargar con pydantic-settings:**
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Testing

#### Estructura de Tests (futuro)
```
tests/
├── test_api/
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_items.py
├── test_models/
└── conftest.py
```

#### Ejecutar Tests
```bash
# Cuando se implementen
pytest
pytest -v  # Verbose
pytest tests/test_api/test_auth.py  # Archivo específico
```

---

## 🔐 Seguridad - Implementación Actual

### Argon2id para Passwords

**Configuración actual** (en `app/core/security.py`):
```python
from argon2 import PasswordHasher

ph = PasswordHasher()  # Usa defaults seguros
```

**Defaults actuales:**
- `time_cost=3` (iteraciones)
- `memory_cost=65536` (64 MB)
- `parallelism=4` (threads)
- Algoritmo: **Argon2id** (recomendado)

**NO modificar** estos parámetros sin consultar Context7 primero.

### JWT Bearer Tokens

**Flujo:**
1. Usuario hace POST `/auth/login` con username + password
2. Backend valida credenciales
3. Retorna JWT token con expiración
4. Cliente incluye token en header: `Authorization: Bearer <token>`
5. Endpoint protegidos verifican token con `CurrentUser` dependency

---


## 🚀 Comandos Útiles

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Crear superusuario
python create_superuser.py
```

### Base de Datos

```bash
# Crear migración
alembic revision --autogenerate -m "Description"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history

# Revertir
alembic downgrade -1
```

### Testing (cuando se implemente)

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Solo un módulo
pytest tests/test_api/test_auth.py -v
```

---

## 📦 Dependencias del Proyecto

Ver `requirements.txt` para versiones exactas:

**Core:**
- fastapi>=0.115.0
- uvicorn[standard]>=0.30.0
- sqlmodel>=0.0.22
- psycopg2-binary>=2.9.9

**Seguridad:**
- argon2-cffi>=23.1.0
- pyjwt>=2.9.0

**Database:**
- alembic>=1.14.0

**Utilidades:**
- pydantic-settings>=2.5.0
- python-multipart>=0.0.12

---

## 🤝 Colaboración

### Antes de Implementar
1. ✅ Leer [MCP-Notion.agent.md](./MCP-Notion.agent.md) - Flujo de trabajo
2. ✅ Obtener tarea de Notion
3. ✅ Consultar Context7 para librerías relevantes
4. ✅ Crear plan con `manage_todo_list`

### Durante Implementación
1. ✅ Seguir convenciones de código de este archivo
2. ✅ Verificar errores frecuentemente con `get_errors`
3. ✅ Actualizar Notion con progreso
4. ✅ Crear migraciones para cambios de BD

### Al Finalizar
1. ✅ Crear PR siguiendo template de MCP-Notion.agent.md
2. ✅ Referenciar tarea de Notion
3. ✅ Incluir checklist de criterios de aceptación
4. ✅ Actualizar estado en Notion a "In Review"

---

## 📚 Referencias

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Alembic Docs**: https://alembic.sqlalchemy.org
- **Argon2-cffi Docs**: https://argon2-cffi.readthedocs.io
- **Context7**: Usar MCP para documentación actualizada

---

> **Recuerda**: Este archivo contiene reglas **específicas del proyecto**. Para el flujo de trabajo con MCPs (Notion, GitHub, Context7), consulta [MCP-Notion.agent.md](./MCP-Notion.agent.md).

