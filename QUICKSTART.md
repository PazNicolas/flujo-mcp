# ⚡ Quick Start - Flujo MCP

Guía ultra-rápida para empezar en 5 minutos.

---

## 🚀 Opción 1: Desarrollo Local (Recomendado)

```bash
# 1. Setup automático (todo en uno)
make setup

# 2. Ejecutar servidor
make dev

# 3. Visitar http://localhost:8000/docs
```

**¡Listo!** Ya tienes:
- ✅ PostgreSQL corriendo en Docker
- ✅ Redis corriendo en Docker
- ✅ pgAdmin disponible en http://localhost:5050
- ✅ API corriendo en http://localhost:8000

---

## 🐳 Opción 2: Todo en Docker

```bash
# 1. Levantar stack completo
make docker-up

# 2. Ver logs
make docker-logs

# 3. Visitar http://localhost:8000/docs
```

**¡Listo!** Todo corriendo en contenedores.

---

## 🧪 Ejecutar Tests

```bash
# Tests básicos
make test

# Tests con coverage
make test-cov
```

---

## 📊 Servicios Disponibles

Una vez levantados los servicios:

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **API** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **PostgreSQL** | localhost:5432 | postgres/postgres |
| **Redis** | localhost:6379 | - |
| **pgAdmin** | http://localhost:5050 | admin@flujo-mcp.local / admin |

---

## 🔑 Crear Usuario

### Crear superusuario:
```bash
make superuser
```

### Registrar usuario normal (API):
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "miusuario",
    "password": "password123",
    "full_name": "Mi Nombre"
  }'
```

---

## 🛠️ Comandos Esenciales

```bash
make help          # Ver todos los comandos
make dev           # Servidor en desarrollo
make deps-up       # Solo dependencias Docker
make deps-down     # Detener dependencias
make test          # Ejecutar tests
make clean         # Limpiar archivos temporales
```

---

## 📚 Documentación Completa

- **README.md** - Guía principal
- **README_DOCKER.md** - Todo sobre Docker
- **README_TESTING.md** - Todo sobre tests
- **CHANGELOG_SETUP.md** - Lista de archivos creados

---

## ❓ Problemas Comunes

### Puerto 8000 en uso
```bash
# Cambiar puerto en .env
# O matar el proceso usando el puerto
lsof -ti:8000 | xargs kill -9
```

### Base de datos no conecta
```bash
# Verificar que Docker esté corriendo
docker ps

# Verificar logs de PostgreSQL
make deps-logs
```

### Tests fallan
```bash
# Limpiar caché y reinstalar
make clean
make install
```

---

## 🎯 Próximos Pasos

1. ✅ Setup completo → `make setup`
2. ✅ Crear superusuario → `make superuser`
3. ✅ Ejecutar tests → `make test`
4. ✅ Explorar API → http://localhost:8000/docs
5. ✅ Leer documentación completa → README.md

---

**¿Necesitas ayuda?** Lee la documentación completa en los archivos README_*.md
