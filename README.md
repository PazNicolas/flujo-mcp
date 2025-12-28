# Flujo-MCP: API con Integración MCP

## 🎯 Descripción del Proyecto

**Flujo-MCP** es una aplicación FastAPI moderna que integra SQLModel, Alembic y autenticación JWT. Este proyecto es una **prueba de concepto de integración de MCP (Model Context Protocol) con programación agéntica**, demostrando cómo los agentes de IA pueden interactuar con sistemas backend robustos y APIs RESTful.

### 🤖 Características de la Integración MCP

Este proyecto demuestra:
- **Programación Agéntica**: Desarrollo asistido por IA usando MCP para crear una API completa
- **Model Context Protocol**: Integración de herramientas de contexto para comunicación entre agentes y sistemas
- **Desarrollo Moderno**: Stack completo con FastAPI, PostgreSQL, y arquitectura limpia
- **Automatización**: Migraciones de base de datos, autenticación JWT, y gestión de usuarios

### 🚀 Tecnologías Principales

- **FastAPI**: Framework web moderno y de alto rendimiento
- **SQLModel**: ORM con integración Pydantic para validación de datos
- **Alembic**: Gestión de migraciones de base de datos
- **JWT Authentication**: Autenticación segura basada en tokens
- **PostgreSQL**: Base de datos relacional robusta

## Requisitos

- Python 3.11+
- PostgreSQL (corriendo en Docker)

## Instalación

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:

El archivo `.env` ya está configurado para conectarse a PostgreSQL en localhost.
Asegúrate de que tu base de datos "flujo-mcp" existe.

## Base de Datos

### Crear la base de datos (si no existe)

```bash
# Conectarse a PostgreSQL y crear la base de datos
psql -U postgres -h localhost -c "CREATE DATABASE \"flujo-mcp\";"
```

### Migraciones con Alembic

```bash
# Crear una nueva migración (autogenerate)
alembic revision --autogenerate -m "Descripción de la migración"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current
```

## Ejecutar la aplicación

```bash
# Modo desarrollo con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentación de la API

Una vez que la aplicación esté corriendo:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login` | Iniciar sesión (obtener token JWT) |
| POST | `/api/auth/logout` | Cerrar sesión |
| GET | `/api/auth/me` | Obtener información del usuario actual |

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/users/` | Registrar nuevo usuario |
| GET | `/api/users/` | Listar usuarios (solo superuser) |
| GET | `/api/users/me` | Obtener perfil del usuario actual |
| PATCH | `/api/users/me` | Actualizar perfil del usuario actual |
| GET | `/api/users/{id}` | Obtener usuario por ID (solo superuser) |
| PATCH | `/api/users/{id}` | Actualizar usuario (solo superuser) |
| DELETE | `/api/users/{id}` | Eliminar usuario (solo superuser) |

## Estructura del Proyecto

```
flujo-mcp/
├── alembic/
│   ├── versions/           # Migraciones de base de datos
│   ├── env.py              # Configuración de Alembic
│   └── script.py.mako      # Template para migraciones
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py     # Endpoints de autenticación
│   │   │   └── users.py    # CRUD de usuarios
│   │   └── deps.py         # Dependencias (auth, session)
│   ├── core/
│   │   ├── config.py       # Configuración con Pydantic Settings
│   │   ├── database.py     # Configuración de la base de datos
│   │   └── security.py     # Utilidades JWT y hashing
│   ├── models/
│   │   └── user.py         # Modelo de usuario SQLModel
│   ├── schemas/
│   │   └── token.py        # Schemas de tokens
│   └── main.py             # Punto de entrada de la aplicación
├── .env                    # Variables de entorno
├── alembic.ini             # Configuración de Alembic
├── requirements.txt        # Dependencias de Python
└── README.md
```

## Ejemplo de uso

### Registrar un usuario

```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "myuser",
    "password": "password123",
    "full_name": "Mi Usuario"
  }'
```

### Iniciar sesión

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=myuser&password=password123"
```

### Obtener perfil (con token)

```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Crear un superusuario

Para crear un superusuario manualmente, puedes usar el siguiente script:

```python
# create_superuser.py
from sqlmodel import Session
from app.core.database import engine
from app.core.security import get_password_hash
from app.models.user import User

with Session(engine) as session:
    superuser = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        full_name="Administrator",
        is_superuser=True,
    )
    session.add(superuser)
    session.commit()
    print("Superuser created!")
```

Ejecutar con: `python create_superuser.py`
