# Instrucciones para Agentes de IA - Flujo MCP

## 🎯 Propósito del Proyecto

Este proyecto es una aplicación FastAPI que sirve como banco de pruebas para flujos de trabajo automatizados usando Model Context Protocol (MCP). El objetivo es demostrar cómo los agentes de IA pueden:

1. Obtener requerimientos desde Notion
2. Implementar código de forma autónoma
3. Crear Pull Requests en GitHub
4. Documentar cambios automáticamente

---

## 🔧 MCPs Disponibles y Su Uso

### 1. Context7 (OBLIGATORIO)

**Siempre usar Context7 antes de implementar cualquier código.**

```
Antes de escribir código, SIEMPRE:
1. Resolver el library ID: mcp_io_github_ups_resolve-library-id
2. Obtener documentación: mcp_io_github_ups_get-library-docs
```

**Librerías principales del proyecto:**
- `/fastapi/fastapi` - Framework web
- `/websites/sqlmodel_tiangolo` - ORM y modelos
- `/sqlalchemy/alembic` - Migraciones de base de datos
- `/hynek/argon2-cffi` - Hashing de contraseñas

### 2. Notion MCP

**Uso:** Gestión de tareas, requerimientos y documentación.

**Funciones principales:**
- `mcp_notion_search` - Buscar páginas y bases de datos
- `mcp_notion_get_page` - Obtener contenido de una página
- `mcp_notion_get_database` - Obtener items de una base de datos
- `mcp_notion_create_page` - Crear nuevas páginas
- `mcp_notion_update_page` - Actualizar páginas existentes

**Flujo de trabajo con Notion:**
1. Buscar la base de datos de tareas/tickets
2. Filtrar por estado (To Do, In Progress, etc.)
3. Obtener detalles de la tarea asignada
4. Actualizar estado cuando se inicie/complete

### 3. GitHub MCP

**Uso:** Gestión de código, branches y Pull Requests.

**Funciones principales:**
- `mcp_github_create_branch` - Crear rama para la tarea
- `mcp_github_create_or_update_file` - Crear/modificar archivos
- `mcp_github_create_pull_request` - Crear PR
- `mcp_github_get_file_contents` - Leer archivos del repo
- `mcp_github_push_files` - Subir múltiples archivos

**Convención de ramas:**
- Features: `feature/TASK-XXX-descripcion-corta`
- Bugfixes: `fix/TASK-XXX-descripcion-corta`
- Hotfixes: `hotfix/TASK-XXX-descripcion-corta`

---

## 📋 Flujo de Trabajo del Agente

### Paso 1: Obtener Tarea de Notion
```
1. Buscar en la base de datos de tareas
2. Identificar tareas con estado "To Do" o asignadas
3. Leer los detalles completos de la tarea
4. Extraer: título, descripción, criterios de aceptación, archivos afectados
```

### Paso 2: Investigar con Context7
```
1. Identificar librerías/frameworks necesarios
2. Buscar documentación actualizada en Context7
3. Revisar ejemplos de código relevantes
4. Verificar mejores prácticas actuales
```

### Paso 3: Planificar Implementación
```
1. Crear lista de TODOs con manage_todo_list
2. Identificar archivos a crear/modificar
3. Determinar orden de implementación
4. Considerar tests necesarios
```

### Paso 4: Implementar Código
```
1. Crear rama en GitHub (si aplica)
2. Implementar cambios siguiendo los TODOs
3. Verificar errores con get_errors
4. Ejecutar tests si existen
```

### Paso 5: Crear Pull Request
```
1. Usar GitHub MCP para crear PR
2. Incluir:
   - Referencia a la tarea de Notion
   - Descripción de cambios
   - Checklist de criterios de aceptación
3. Actualizar estado en Notion a "In Review"
```

---

## 📝 Convenciones de Código

### Python
- **Formateo:** Black, líneas de 88 caracteres
- **Imports:** isort, agrupados por stdlib/third-party/local
- **Typing:** Usar type hints en todas las funciones
- **Docstrings:** Google style

### API Endpoints
- **Verbos REST:** GET (leer), POST (crear), PATCH (actualizar), DELETE (eliminar)
- **Respuestas:** Usar response_model para validación
- **Errores:** HTTPException con códigos apropiados

### Base de Datos
- **Migraciones:** Siempre usar Alembic, nunca modificar DB directamente
- **Modelos:** Separar modelos de tabla de schemas de request/response

---

## ⚠️ Reglas Importantes

1. **SIEMPRE consultar Context7** antes de implementar código con librerías
2. **NUNCA hardcodear** credenciales o secretos
3. **SIEMPRE crear migraciones** para cambios en modelos de DB
4. **SIEMPRE verificar errores** después de editar archivos
5. **Documentar** funciones y endpoints complejos
6. **Actualizar Notion** con el progreso de la tarea

---

## 🔐 Seguridad

- Passwords hasheados con Argon2id
- Autenticación via JWT Bearer tokens
- Variables sensibles en `.env` (no commitear)
- Validación de inputs con Pydantic
