# Flujo de Trabajo MCP - Guía Completa

Este documento describe cómo utilizar los diferentes MCPs para automatizar el desarrollo de software con agentes de IA.

---

## 📚 MCP Context7 - Documentación de Librerías

### ¿Qué es?
Context7 proporciona acceso a documentación actualizada de miles de librerías de programación. Es **obligatorio** usarlo antes de implementar código para asegurar que se usan las APIs más recientes.

### Cuándo Usarlo
- Antes de implementar cualquier funcionalidad nueva
- Cuando necesites ejemplos de código actualizados
- Para verificar la sintaxis correcta de una librería
- Cuando encuentres errores con una API

### Cómo Usarlo

#### Paso 1: Resolver el ID de la Librería
```
Herramienta: mcp_io_github_ups_resolve-library-id
Parámetro: libraryName = "nombre de la librería"

Ejemplo: "FastAPI", "SQLModel", "argon2-cffi"
```

#### Paso 2: Obtener Documentación
```
Herramienta: mcp_io_github_ups_get-library-docs
Parámetros:
  - context7CompatibleLibraryID: "/org/project" (del paso anterior)
  - topic: "tema específico a buscar"
  - mode: "code" (ejemplos) o "info" (conceptual)
```

### Ejemplos de Uso

**Buscar autenticación JWT en FastAPI:**
```
1. resolve-library-id: "FastAPI"
   → Resultado: /fastapi/fastapi

2. get-library-docs:
   - context7CompatibleLibraryID: "/fastapi/fastapi"
   - topic: "JWT authentication OAuth2"
   - mode: "code"
```

**Buscar migraciones en Alembic:**
```
1. resolve-library-id: "Alembic"
   → Resultado: /sqlalchemy/alembic

2. get-library-docs:
   - context7CompatibleLibraryID: "/sqlalchemy/alembic"
   - topic: "autogenerate migration"
   - mode: "code"
```

---

## 📋 MCP Notion - Gestión de Tareas

### ¿Qué es?
Notion MCP permite interactuar con workspaces de Notion para leer y escribir páginas, bases de datos y gestionar tareas como un sistema de tickets.

### Estructura Recomendada en Notion

#### Base de Datos de Tareas
Crear una base de datos con estas propiedades:

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| Título | Title | Nombre de la tarea |
| ID | Text | Identificador único (TASK-001) |
| Estado | Select | To Do, In Progress, In Review, Done |
| Prioridad | Select | Low, Medium, High, Critical |
| Tipo | Select | Feature, Bug, Hotfix, Refactor |
| Asignado | Person | Responsable de la tarea |
| Sprint | Relation | Sprint al que pertenece |
| Archivos Afectados | Multi-select | Rutas de archivos a modificar |
| PR Link | URL | Link al Pull Request |

### Funciones Principales

#### Buscar Base de Datos
```
Herramienta: mcp_notion_search
Parámetro: query = "Tareas" o "Tasks"
```

#### Obtener Tareas
```
Herramienta: mcp_notion_get_database
Parámetros:
  - database_id: "id-de-la-base-de-datos"
  - filter: { "property": "Estado", "select": { "equals": "To Do" } }
```

#### Leer Detalles de Tarea
```
Herramienta: mcp_notion_get_page
Parámetro: page_id = "id-de-la-pagina"
```

#### Actualizar Estado
```
Herramienta: mcp_notion_update_page
Parámetros:
  - page_id: "id-de-la-pagina"
  - properties: { "Estado": { "select": { "name": "In Progress" } } }
```

---

## 🐙 MCP GitHub - Control de Versiones

### ¿Qué es?
GitHub MCP permite interactuar con repositorios de GitHub para crear ramas, commits, pull requests y gestionar código.

### Funciones Principales

#### Crear Rama
```
Herramienta: mcp_github_create_branch
Parámetros:
  - owner: "tu-usuario"
  - repo: "flujo-mcp"
  - branch: "feature/TASK-001-nueva-funcionalidad"
  - from_branch: "main" (opcional)
```

#### Crear/Actualizar Archivo
```
Herramienta: mcp_github_create_or_update_file
Parámetros:
  - owner: "tu-usuario"
  - repo: "flujo-mcp"
  - path: "app/api/routes/nuevo.py"
  - content: "contenido del archivo"
  - message: "feat(api): add new endpoint"
  - branch: "feature/TASK-001-nueva-funcionalidad"
```

#### Subir Múltiples Archivos
```
Herramienta: mcp_github_push_files
Parámetros:
  - owner: "tu-usuario"
  - repo: "flujo-mcp"
  - branch: "feature/TASK-001"
  - files: [
      { "path": "file1.py", "content": "..." },
      { "path": "file2.py", "content": "..." }
    ]
  - message: "feat: implement TASK-001"
```

#### Crear Pull Request
```
Herramienta: mcp_github_create_pull_request
Parámetros:
  - owner: "tu-usuario"
  - repo: "flujo-mcp"
  - title: "feat(api): TASK-001 - Nueva funcionalidad"
  - body: "## Descripción\n..."
  - head: "feature/TASK-001-nueva-funcionalidad"
  - base: "main"
```

### Formato de Commits (Conventional Commits)

```
<tipo>(<scope>): <descripción>

Tipos:
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Documentación
- refactor: Refactorización
- test: Tests
- chore: Mantenimiento
```

---

## 🔄 Flujo Completo de Ejemplo

### Escenario: Implementar endpoint de perfil de usuario

```
1. NOTION: Buscar tarea asignada
   → mcp_notion_search("Tareas")
   → mcp_notion_get_database(database_id, filter: "To Do")
   → Encontrar: TASK-005 "Endpoint de perfil de usuario"

2. NOTION: Leer detalles
   → mcp_notion_get_page(page_id)
   → Extraer: descripción, criterios, archivos afectados

3. NOTION: Actualizar estado
   → mcp_notion_update_page(page_id, status: "In Progress")

4. CONTEXT7: Investigar implementación
   → resolve-library-id("FastAPI")
   → get-library-docs("/fastapi/fastapi", topic: "response model pydantic")

5. LOCAL: Implementar código
   → Crear/modificar archivos
   → Verificar errores
   → Crear migración si es necesario

6. GITHUB: Crear rama y PR
   → mcp_github_create_branch("feature/TASK-005-user-profile")
   → mcp_github_push_files(archivos modificados)
   → mcp_github_create_pull_request(...)

7. NOTION: Actualizar con PR
   → mcp_notion_update_page(page_id, status: "In Review", pr_link: "...")
```

---

## ⚡ Tips para Agentes

1. **Siempre empieza con Context7** - La documentación actualizada evita errores
2. **Lee la tarea completa** - No asumas, verifica los criterios de aceptación
3. **Actualiza el estado en Notion** - Mantén visibilidad del progreso
4. **Commits atómicos** - Un cambio lógico por commit
5. **PR descriptivos** - Incluye contexto, screenshots si aplica
6. **Verifica antes de pushear** - Usa get_errors para validar
