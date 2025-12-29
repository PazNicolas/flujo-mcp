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
- Docker y Docker Compose (para dependencias locales)

## Inicio Rápido

### Opción A: Setup Automático con Make

```bash
# Setup completo (crea .env, instala deps, levanta Docker, aplica migraciones)
make setup

# Ejecutar servidor de desarrollo
make dev
```

### Opción B: Setup Manual

### 1. Levantar dependencias locales (PostgreSQL, Redis, pgAdmin)

```bash
# Iniciar servicios
docker-compose -f local-deps.yml up -d

# Verificar que los servicios estén corriendo
docker-compose -f local-deps.yml ps

# Ver logs si es necesario
docker-compose -f local-deps.yml logs -f
```

**Acceso a servicios:**
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`
- **pgAdmin**: http://localhost:5050
  - Email: `admin@flujo-mcp.local`
  - Password: `admin`

### 2. Configurar el entorno Python

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env si necesitas cambiar alguna configuración
# Por defecto está configurado para conectarse a los servicios de Docker
```

## Base de Datos

### Aplicar migraciones

```bash
# La base de datos se crea automáticamente al levantar Docker
# Solo necesitas aplicar las migraciones

# Aplicar migraciones
alembic upgrade head

# Crear un superusuario (opcional)
python create_superuser.py
```

### Comandos de Alembic

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

### Modo desarrollo

```bash
# Modo desarrollo con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Con Docker

```bash
# Construir la imagen
docker build -t flujo-mcp:latest .

# Ejecutar el contenedor
docker run -d \
  --name flujo-mcp-api \
  --network flujo-mcp-network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@flujo-mcp-postgres:5432/flujo-mcp \
  -e REDIS_URL=redis://flujo-mcp-redis:6379/0 \
  flujo-mcp:latest
```

## Testing

```bash
# Instalar dependencias de testing (si no están instaladas)
pip install pytest pytest-cov

# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pytest --cov=app --cov-report=html

# Ejecutar tests específicos
pytest tests/test_auth.py
pytest tests/test_users.py -v

# Ejecutar solo tests rápidos (excluir lentos)
pytest -m "not slow"
```

## Detener servicios

```bash
# Con Make
make deps-down

# Con Docker Compose
docker-compose -f local-deps.yml down

# Detener y eliminar volúmenes (⚠️ esto borrará los datos)
docker-compose -f local-deps.yml down -v
```

## 🛠️ Comandos Útiles (Makefile)

El proyecto incluye un Makefile con comandos útiles:

```bash
make help          # Mostrar todos los comandos disponibles
make setup         # Setup inicial completo
make dev           # Ejecutar servidor en desarrollo
make deps-up       # Levantar dependencias Docker
make deps-down     # Detener dependencias
make test          # Ejecutar tests
make test-cov      # Tests con coverage
make db-upgrade    # Aplicar migraciones
make db-migrate    # Crear nueva migración
make superuser     # Crear superusuario
make clean         # Limpiar archivos temporales
make docker-up     # Levantar stack completo
make docker-down   # Detener stack completo
```

## Documentación de la API

Una vez que la aplicación esté corriendo:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Documentación Adicional

- **[README_DOCKER.md](README_DOCKER.md)** - Guía completa de Docker (comandos, troubleshooting, deployment)
- **[README_TESTING.md](README_TESTING.md)** - Guía de testing (escribir tests, coverage, CI/CD)
- **[.github/agents/MCP-Notion.agent.md](.github/agents/MCP-Notion.agent.md)** - Flujo de trabajo con MCPs
- **[.github/instructions.md](.github/instructions.md)** - Convenciones y stack del proyecto

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
├── .github/
│   ├── agents/
│   │   └── MCP-Notion.agent.md    # Flujo de trabajo con MCPs
│   └── instructions.md            # Convenciones del proyecto
├── alembic/
│   ├── versions/                  # Migraciones de base de datos
│   ├── env.py                     # Configuración de Alembic
│   └── script.py.mako            # Template para migraciones
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py           # Endpoints de autenticación
│   │   │   ├── items.py          # CRUD de items
│   │   │   └── users.py          # CRUD de usuarios
│   │   └── deps.py               # Dependencias (auth, session)
│   ├── core/
│   │   ├── config.py             # Configuración con Pydantic Settings
│   │   ├── database.py           # Configuración de la base de datos
│   │   ├── redis.py              # Cliente de Redis
│   │   └── security.py           # Utilidades JWT y hashing
│   ├── models/
│   │   ├── item.py               # Modelo de items
│   │   └── user.py               # Modelo de usuario SQLModel
│   ├── schemas/
│   │   └── token.py              # Schemas de tokens
│   └── main.py                   # Punto de entrada de la aplicación
├── tests/
│   ├── conftest.py               # Fixtures de pytest
│   ├── test_auth.py              # Tests de autenticación
│   ├── test_items.py             # Tests de items
│   ├── test_main.py              # Tests de endpoints principales
│   └── test_users.py             # Tests de usuarios
├── .env.example                  # Ejemplo de variables de entorno
├── .gitignore                    # Archivos ignorados por git
├── alembic.ini                   # Configuración de Alembic
├── create_superuser.py           # Script para crear superusuario
├── docker-compose.yml            # Stack completo (app + deps)
├── Dockerfile                    # Imagen Docker de la aplicación
├── local-deps.yml                # Solo dependencias (PostgreSQL, Redis, pgAdmin)
├── pytest.ini                    # Configuración de pytest
├── README.md                     # Este archivo
├── README_DOCKER.md              # Guía de Docker
├── README_TESTING.md             # Guía de testing
└── requirements.txt              # Dependencias de Python
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

Ya existe un script para crear superusuarios:

```bash
# Ejecutar el script interactivo
python create_superuser.py
```

## Características de Seguridad

- ✅ **Autenticación JWT** con access y refresh tokens
- ✅ **Hashing con Argon2id** (ganador del Password Hashing Competition)
- ✅ **Rate limiting** con Redis (protección contra brute force)
- ✅ **Bloqueo de cuentas** tras múltiples intentos fallidos
- ✅ **Token blacklisting** para logout seguro
- ✅ **Separación de permisos** (user vs superuser)

## Roadmap

- [ ] Verificación de email
- [ ] Reset de contraseña
- [ ] Sistema de roles más granular
- [ ] Auditoría de acciones
- [ ] API de notificaciones
- [ ] Integración completa con Notion MCP
- [ ] CI/CD con GitHub Actions
- [ ] Documentación de API mejorada

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

Desarrollado como prueba de concepto de **programación agéntica** con **Model Context Protocol (MCP)** 🤖
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
