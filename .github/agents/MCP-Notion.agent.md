# Flujo de Trabajo con MCP para Agentes de IA

> **Archivo estándar de la organización** - Define el flujo de trabajo agnóstico a la tecnología para automatización con MCPs.
> Este archivo trabaja en conjunto con `instructions.md` que contiene las reglas específicas de cada proyecto.

---

## 🎯 Objetivo

Este documento define el flujo de trabajo estándar para agentes de IA que trabajan con:
- **Notion MCP**: Gestión de tareas y requerimientos
- **GitHub MCP**: Control de versiones y Pull Requests
- **Context7**: Documentación actualizada de librerías

---

## 🔧 MCPs Disponibles

### 1. Context7 (OBLIGATORIO)

**⚠️ Siempre usar Context7 antes de implementar cualquier código.**

**Proceso obligatorio:**
```
Antes de escribir código, SIEMPRE:
1. Resolver el library ID: mcp_io_github_ups_resolve-library-id
2. Obtener documentación: mcp_io_github_ups_get-library-docs
```

**¿Por qué Context7?**
- Obtiene documentación actualizada directamente de los repositorios oficiales
- Evita usar información obsoleta o incorrecta
- Proporciona ejemplos de código actuales y mejores prácticas
- Reduce errores de implementación

**Cuándo usar:**
- Antes de implementar funcionalidades con librerías externas
- Al actualizar dependencias
- Cuando necesites verificar APIs o métodos específicos
- Para validar mejores prácticas de seguridad

---

### 2. Notion MCP

**Uso:** Gestión de tareas, requerimientos y documentación.

**Herramientas principales:**
- `notion-search` - Buscar en workspace y herramientas conectadas (Slack, Google Drive, Jira)
- `notion-fetch` - Obtener contenido de página o base de datos por URL
- `notion-create-pages` - Crear una o más páginas con propiedades y contenido
- `notion-update-page` - Actualizar propiedades o contenido de páginas
- `notion-move-pages` - Mover páginas o bases de datos a nuevo padre
- `notion-duplicate-page` - Duplicar página (async)
- `notion-create-database` - Crear nueva base de datos con propiedades
- `notion-update-database` - Actualizar propiedades de data source
- `notion-query-data-sources` - Consultar múltiples data sources (Enterprise + AI)
- `notion-create-comment` - Agregar comentario a página
- `notion-get-comments` - Listar comentarios de página
- `notion-get-teams` - Obtener lista de equipos (teamspaces)
- `notion-get-users` - Listar usuarios del workspace
- `notion-get-user` - Obtener información de usuario por ID
- `notion-get-self` - Información del bot user actual

**Flujo de trabajo con Notion:**

1. **Búsqueda de tareas:**
   - Buscar la base de datos de tareas/tickets del proyecto
   - Usar filtros por estado (To Do, In Progress, Blocked)
   - Identificar tareas asignadas o priorizadas

2. **Obtención de detalles:**
   - Leer descripción completa de la tarea
   - Extraer criterios de aceptación
   - Identificar dependencias o archivos relacionados
   - Revisar comentarios y contexto adicional

3. **Actualización de estado:**
   - Al iniciar: Cambiar estado a "In Progress"
   - Durante desarrollo: Actualizar con comentarios de progreso
   - Al completar: Cambiar a "In Review" o "Done"
   - En caso de bloqueos: Marcar como "Blocked" con razón

**⚠️ Límites de Rate:**
- General: 180 requests/minuto (3 req/segundo)
- Search específico: 30 requests/minuto
- Si encuentras rate limits: reduce búsquedas paralelas y espera

**💡 Capacidades especiales:**
- `notion-search` con Notion AI: busca en Slack, Google Drive, GitHub, Jira, etc.
- `notion-query-data-sources`: consultas estructuradas multi-database (Enterprise + AI)
- Sin AI: búsqueda limitada solo al workspace de Notion

---

### 3. GitHub MCP

**Uso:** Gestión de código, branches y Pull Requests.

**Toolsets disponibles:**
- `context` - Información del usuario y contexto actual (recomendado)
- `repos` - Gestión de repositorios y archivos
- `issues` - Creación y gestión de issues
- `pull_requests` - Gestión de Pull Requests
- `actions` - GitHub Actions y CI/CD
- `code_security` - Code scanning y seguridad
- `discussions` - GitHub Discussions
- `gists` - Gestión de Gists
- `git` - Operaciones Git de bajo nivel
- `projects` - GitHub Projects
- `users` - Información de usuarios
- `stargazers` - Gestión de stars
- Y más: `dependabot`, `labels`, `notifications`, `orgs`, `secret_protection`, `security_advisories`

**Herramientas clave:**
- Repositorios: `get_file_contents`, `create_or_update_file`, `push_files`, `search_code`
- Branches: `create_branch`, `list_branches`, `get_branch`
- Pull Requests: `create_pull_request`, `update_pull_request`, `merge_pull_request`, `search_pull_requests`
- Issues: `create_issue`, `update_issue`, `list_issues`, `search_issues`
- Commits: `get_commit`, `list_commits`

**Convención de ramas estándar:**
```
feature/TASK-XXX-descripcion-corta  # Nuevas funcionalidades
fix/TASK-XXX-descripcion-corta      # Corrección de bugs
hotfix/TASK-XXX-descripcion-corta   # Correcciones urgentes
refactor/TASK-XXX-descripcion-corta # Refactorización de código
docs/TASK-XXX-descripcion-corta     # Documentación
```

**Formato de descripción:** kebab-case, máximo 50 caracteres

**Configuración de toolsets:**
```bash
# Default toolsets (si no especificas ninguno):
# context, repos, issues, pull_requests, users

# Especificar toolsets específicos:
--toolsets repos,issues,pull_requests,actions

# Habilitar todos:
--toolsets all

# Modo solo lectura:
--read-only

# Herramientas individuales:
--tools get_file_contents,issue_read,create_pull_request
```

**Modos especiales:**
- `--read-only`: Solo operaciones de lectura, sin modificaciones
- `--dynamic-toolsets`: Descubrimiento dinámico de toolsets (beta, no en remote)
- `--lockdown-mode`: Limita contenido de repos públicos (solo autores con push access)

---

## 📋 Flujo de Trabajo Completo

### Fase 1: Obtener y Analizar Tarea

```
PASO 1: Buscar tareas pendientes en Notion
  - Usar mcp_makenotion_no_notion-search con query apropiado
  - Filtrar por estado "To Do" o tareas asignadas
  - Priorizar según urgencia/prioridad

PASO 2: Leer detalles completos
  - Usar mcp_makenotion_no_notion-fetch para obtener contenido
  - Extraer información clave:
    * Título y descripción
    * Criterios de aceptación
    * Archivos a modificar/crear
    * Dependencias o limitaciones
    * Links relacionados

PASO 3: Actualizar estado en Notion
  - Cambiar estado a "In Progress"
  - Agregar comentario con timestamp de inicio
```

---

### Fase 2: Investigar y Planificar

```
PASO 1: Identificar dependencias técnicas
  - Listar librerías/frameworks necesarios
  - Identificar versiones actuales en el proyecto

PASO 2: Consultar Context7 (OBLIGATORIO)
  - Para CADA librería externa:
    a) Resolver library ID con mcp_io_github_ups_resolve-library-id
    b) Obtener documentación con mcp_io_github_ups_get-library-docs
    c) Buscar ejemplos relevantes al caso de uso
    d) Verificar mejores prácticas de seguridad

PASO 3: Crear plan de implementación
  - Usar manage_todo_list para crear checklist
  - Desglosar tarea en pasos concretos y verificables
  - Identificar orden óptimo de implementación
  - Considerar necesidad de tests
```

---

### Fase 3: Implementar Código

```
PASO 1: Preparar entorno Git
  - Crear branch siguiendo convención de nombres
  - Usar mcp_io_github_git_create_branch desde main/develop

PASO 2: Implementar cambios
  - Seguir el plan de TODOs creado
  - Marcar cada TODO como "in-progress" al iniciarlo
  - Marcar como "completed" al terminarlo
  - Verificar errores con get_errors después de cada cambio

PASO 3: Validar implementación
  - Ejecutar tests si existen
  - Verificar que no hay errores de linting/typing
  - Confirmar que se cumplen criterios de aceptación
```

---

### Fase 4: Crear Pull Request

```
PASO 1: Preparar PR
  - Revisar todos los cambios realizados
  - Asegurar que el código sigue convenciones del proyecto
  - Verificar que la documentación está actualizada

PASO 2: Crear PR en GitHub
  - Usar mcp_io_github_git_create_pull_request
  - Incluir en la descripción:
    * Link a la tarea de Notion
    * Resumen de cambios realizados
    * Checklist de criterios de aceptación
    * Instrucciones de prueba (si aplica)
    * Screenshots/demos (si aplica)

PASO 3: Actualizar Notion
  - Cambiar estado a "In Review"
  - Agregar link al PR creado
  - Comentar resumen de implementación
```

---

### Fase 5: Seguimiento Post-PR

```
PASO 1: Monitorear revisiones
  - Revisar comentarios de code review
  - Responder preguntas o solicitudes de cambios

PASO 2: Aplicar correcciones si es necesario
  - Crear commits adicionales en la misma rama
  - Actualizar PR con explicación de cambios

PASO 3: Cierre de tarea
  - Al hacer merge: Actualizar Notion a "Done"
  - Agregar comentarios finales o lecciones aprendidas
  - Cerrar branch si no se hace automáticamente
```

---

## ⚠️ Reglas Universales para Todos los Proyectos

### Context7
1. ✅ **SIEMPRE consultar Context7** antes de implementar código con librerías externas
2. ✅ **NUNCA asumir APIs** sin verificar documentación actualizada
3. ✅ **BUSCAR ejemplos** de código en la documentación oficial

### Seguridad
4. ✅ **NUNCA hardcodear** credenciales, tokens, o secretos
5. ✅ **SIEMPRE usar variables de entorno** para configuración sensible
6. ✅ **VALIDAR inputs** de usuarios antes de procesarlos

### Git y GitHub
7. ✅ **SIEMPRE crear branch** para nuevas tareas (nunca commit directo a main)
8. ✅ **NOMBRES descriptivos** para branches y commits
9. ✅ **PRs con contexto completo**: descripción, testing, referencias

### Notion
10. ✅ **ACTUALIZAR estado** de tareas en tiempo real
11. ✅ **DOCUMENTAR bloqueos** inmediatamente cuando ocurran
12. ✅ **AGREGAR links** entre Notion y GitHub para trazabilidad

### Calidad de Código
13. ✅ **VERIFICAR errores** después de cada cambio con get_errors
14. ✅ **SEGUIR convenciones** definidas en instructions.md del proyecto
15. ✅ **EJECUTAR tests** antes de crear PR (si existen)

---

## 🔄 Plantilla de Comentario para Notion

Al actualizar una tarea, usa este formato:

```markdown
**[TIMESTAMP]** - Estado: [In Progress/In Review/Blocked/Done]

**Cambios realizados:**
- [Lista de cambios principales]

**Archivos modificados:**
- [Lista de archivos]

**PR:** [Link al PR] (si aplica)

**Notas:** [Observaciones, decisiones técnicas, bloqueos]

**Siguiente paso:** [Qué sigue]
```

---

## 🔄 Plantilla de Descripción de PR

```markdown
## 🎯 Tarea
Closes: [Link a tarea de Notion]

## 📝 Descripción
[Descripción clara y concisa de los cambios]

## ✅ Criterios de Aceptación
- [ ] [Criterio 1]
- [ ] [Criterio 2]
- [ ] [Criterio N]

## 🧪 Testing
[Cómo probar los cambios]

## 📸 Screenshots/Demos
[Si aplica: capturas o demos visuales]

## 🔗 Referencias
- Documentación Context7: [links usados]
- Issues relacionados: [si aplica]

## ⚠️ Breaking Changes
[Si hay cambios que rompen compatibilidad]

## 📌 Notas adicionales
[Decisiones técnicas, consideraciones, etc.]
```

---

## 🎓 Mejores Prácticas

### Para Context7
- **Especifica el topic**: Al buscar documentación, usa topics específicos para resultados relevantes
- **Revisa versiones**: Asegúrate de que la versión de la documentación coincida con tu proyecto
- **Guarda referencias**: Anota los links de documentación usados para el PR

### Para Notion
- **Actualiza frecuentemente**: No esperes al final del día
- **Sé específico**: Los comentarios vagos no ayudan al equipo
- **Marca bloqueos ASAP**: Si algo te detiene, escálalo inmediatamente

### Para GitHub
- **Commits atómicos**: Un commit = un cambio lógico
- **Mensajes claros**: Usa convencional commits si el proyecto lo requiere
- **PRs pequeños**: Facilita code review y reduce errores

---

## 🚫 Anti-patrones a Evitar

❌ **NO implementar sin consultar Context7 primero**
❌ **NO crear PRs gigantes con múltiples features**
❌ **NO dejar tareas en Notion sin actualizar por horas**
❌ **NO hacer commits directos a main/master**
❌ **NO asumir que la documentación de hace 6 meses sigue vigente**
❌ **NO ignorar errores de linting o typing**
❌ **NO crear branches con nombres genéricos (fix, test, etc.)**

---

## 📚 Referencias Útiles

- **Context7 MCP**: Para documentación actualizada de librerías
- **Notion MCP Docs**: https://developers.notion.com/docs/mcp-supported-tools
- **GitHub MCP Server**: https://github.com/github/github-mcp-server
- **GitHub MCP Toolsets**: Ver tabla completa en README del servidor oficial
- **Convenciones específicas**: Ver `instructions.md` del proyecto

### Instalación de servidores MCP

**Notion MCP:**
- Remote: Hospedado por Notion (más fácil)
- Requiere autenticación OAuth o integración conectada

**GitHub MCP:**
- Remote: `https://api.githubcopilot.com/mcp/` (con OAuth o PAT)
- Local: Docker o binary compilado
- GitHub Enterprise: Soporte para Cloud (ghe.com) y Server

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Buscar y crear página en Notion
```
Usuario: "Busca todas las tareas de alta prioridad y créame un resumen"

Agente:
1. notion-search: query="alta prioridad status:To Do"
2. Analizar resultados
3. notion-create-pages: Crear página de resumen con links
4. Retornar URL de la nueva página
```

### Ejemplo 2: Crear feature completo con GitHub
```
Usuario: "Implementa el endpoint de login según el ticket TASK-123 en Notion"

Agente:
1. notion-fetch: Obtener detalles de TASK-123
2. Context7: Buscar docs de FastAPI y Argon2
3. create_branch: feature/TASK-123-login-endpoint
4. create_or_update_file: Múltiples archivos
5. create_pull_request: Con referencia a TASK-123
6. notion-update-page: Cambiar estado a "In Review"
```

### Ejemplo 3: Code review con GitHub MCP
```
Usuario: "Revisa el PR #45 y deja comentarios"

Agente (con toolset pull_requests):
1. get_pull_request: Obtener detalles del PR #45
2. get_file_contents: Revisar archivos modificados
3. add_comment_to_pending_review: Agregar comentarios
4. submit_review: Enviar review
```

### Ejemplo 4: Query multi-database en Notion (Enterprise)
```
Usuario: "¿Qué tareas críticas están vencidas esta semana?"

Agente (con Notion AI):
1. notion-query-data-sources: 
   - Filter: status="Critical" AND due_date<today
   - Group by: owner
2. Presentar resumen organizado
```

---

> **Nota**: Este documento es agnóstico al lenguaje y framework. Para reglas específicas de tecnología, estilo de código, y estructura del proyecto, consulta el archivo `instructions.md` en cada repositorio.
