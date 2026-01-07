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
   - Usar notion-search para buscar la base de datos de tareas/tickets del proyecto
   - Aplicar filtros por estado (To Do, In Progress, Blocked)
   - Identificar tareas asignadas o priorizadas
   - ⚠️ Si la búsqueda falla, reportar: "Error en notion-search: [mensaje]"

2. **Obtención de detalles:**
   - Usar notion-fetch con el page_id obtenido de la búsqueda
   - Leer descripción completa de la tarea
   - Extraer criterios de aceptación
   - Identificar dependencias o archivos relacionados
   - Revisar comentarios y contexto adicional
   - ⚠️ Si notion-fetch falla, reportar: "No se pudo acceder a la tarea: [mensaje]"
   - ⚠️ NUNCA intentar acceder directamente a URLs de Notion

3. **Actualización de estado:**
   - Obtener page_id mediante notion-fetch si no se tiene
   - Al iniciar: Usar notion-update-page para cambiar estado a "In Progress"
   - Durante desarrollo: Usar notion-create-comment para actualizar progreso
   - Al completar: Usar notion-update-page para cambiar a "In Review" o "Done"
   - En caso de bloqueos: Usar notion-update-page para marcar como "Blocked" y notion-create-comment para explicar
   - ⚠️ Si cualquier operación falla, informar: "Error al actualizar Notion: [herramienta] - [mensaje]"
   - ⚠️ Continuar con el trabajo aunque Notion falle, pero siempre reportar el error

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

## 📋 Flujo de Trabajo en 3 Fases (Multi-Modelo Manual)

> **⚠️ IMPORTANTE:** Este flujo está diseñado para que puedas cambiar manualmente el modelo de IA entre fases según tus necesidades.
> 
> **Sugerencias de modelos por fase:**
> - **FASE 1 (Recuperación de Contexto):** Gemini 2.0 Flash Thinking, Claude Sonnet 4.5
> - **FASE 2 (Planificación):** Claude Opus 4.5, Claude Sonnet 4.5
> - **FASE 3 (Codificación):** Claude Sonnet 4.5, GPT-4o
> 
> 👉 **Cambia el modelo en el dropdown de Chat view ANTES de iniciar cada fase**

---

## 🔍 FASE 1: Recuperación de Contexto desde Notion

**🎯 Objetivo:** Obtener toda la información necesaria de la tarea desde Notion y entender el contexto completo.

**📊 Modelo recomendado:** Gemini 2.0 Flash Thinking (excelente en análisis y razonamiento)

**Pasos a ejecutar:**

### 1.1 Buscar y obtener la tarea

```markdown
ACCIÓN: Buscar tarea en Notion

Herramientas MCP:
- notion-search: Buscar tarea por ID o título
- notion-fetch: Obtener contenido completo de la tarea

⚠️ IMPORTANTE:
- SIEMPRE usar notion-fetch con el ID de la página de Notion
- NUNCA intentar acceder directamente a URLs de Notion
- Si notion-fetch falla, informar el error inmediatamente al usuario
- No intentar métodos alternativos de acceso

Prompt sugerido:
"Busca en Notion la tarea TASK-XXX usando notion-search.
Una vez encontrada, usa notion-fetch con el ID de la página para obtener:
- Título y descripción completa
- Criterios de aceptación
- Dependencias o bloqueadores
- Archivos mencionados
- Comentarios importantes
- Links relacionados

Si el MCP falla en cualquier paso, reportar el error específico."
```

### 1.2 Analizar el contexto del proyecto

```markdown
ACCIÓN: Entender el estado actual del código

Herramientas a usar:
- list_dir: Ver estructura del proyecto
- read_file: Leer archivos relevantes mencionados
- grep_search: Buscar código relacionado
- semantic_search: Buscar contexto similar

Prompt sugerido:
"Analiza el contexto del proyecto:
- Estructura de directorios relevante
- Archivos que serán modificados
- Código existente relacionado
- Patrones y convenciones actuales"
```

### 1.3 Actualizar estado en Notion

```markdown
ACCIÓN: Marcar tarea como "In Progress"

Herramientas MCP:
- notion-update-page: Cambiar estado (requiere ID de página)
- notion-create-comment: Agregar comentario de inicio (requiere page_id)

⚠️ IMPORTANTE:
- SIEMPRE usar el ID de página obtenido de notion-fetch
- NUNCA extraer IDs manualmente de URLs
- Si notion-update-page o notion-create-comment fallan, reportar el error
- Validar que el cambio de estado fue exitoso

Prompt sugerido:
"Usando el ID de página obtenido anteriormente con notion-fetch:
1. Usa notion-update-page para cambiar el estado a 'In Progress'
2. Usa notion-create-comment para agregar: 'Iniciado análisis [fecha/hora]'
3. Si alguna operación falla, reportar el error específico del MCP
4. Confirmar que los cambios se aplicaron correctamente"
```

### ✅ Output esperado de Fase 1:

- ✓ Documento con análisis completo de la tarea
- ✓ Lista de archivos a modificar/crear
- ✓ Identificación de dependencias técnicas
- ✓ Estado actualizado en Notion
- ✓ Contexto claro del código existente

**⏸️ PAUSA AQUÍ - Cambia de modelo antes de continuar a Fase 2**

---

## 📐 FASE 2: Creación del Plan de Implementación

**🎯 Objetivo:** Diseñar un plan detallado de implementación consultando documentación actualizada y mejores prácticas.

**📊 Modelo recomendado:** Claude Opus 4.5 (excelente en arquitectura y planificación)

**Pasos a ejecutar:**

### 2.1 Consultar documentación con Context7

```markdown
ACCIÓN: Obtener documentación actualizada de librerías

Herramientas MCP (OBLIGATORIO):
- mcp_io_github_ups_resolve-library-id: Para cada librería
- mcp_io_github_ups_get-library-docs: Obtener docs actualizadas

Prompt sugerido:
"Para cada librería identificada en Fase 1:
1. Resuelve el library ID en Context7
2. Obtén documentación actualizada
3. Busca ejemplos relevantes al caso de uso
4. Identifica mejores prácticas de seguridad"

Ejemplo:
- FastAPI: /fastapi/fastapi
- SQLModel: /websites/sqlmodel_tiangolo
- Argon2: /hynek/argon2-cffi
```

### 2.2 Crear plan de implementación detallado

```markdown
ACCIÓN: Diseñar plan paso a paso

Herramientas a usar:
- manage_todo_list: Crear checklist estructurado
- read_file: Revisar instructions.md del proyecto

Prompt sugerido:
"Crea un plan de implementación detallado:

1. ANÁLISIS TÉCNICO:
   - Tecnologías y librerías necesarias
   - Versiones compatibles
   - Patrones de diseño a aplicar

2. PASOS DE IMPLEMENTACIÓN (desglosados):
   - Paso 1: [Descripción específica]
   - Paso 2: [Descripción específica]
   - ...

3. ARCHIVOS A MODIFICAR/CREAR:
   - archivo1.py: [Cambios específicos]
   - archivo2.py: [Cambios específicos]
   - ...

4. TESTS NECESARIOS:
   - Test 1: [Qué validar]
   - Test 2: [Qué validar]

5. CRITERIOS DE ACEPTACIÓN:
   - [ ] Criterio 1
   - [ ] Criterio 2
   - ...

6. CONSIDERACIONES DE SEGURIDAD:
   - [Lista de validaciones necesarias]

7. ORDEN DE EJECUCIÓN:
   - Primera: [Tarea]
   - Segunda: [Tarea]
   - ...
"
```

### 2.3 Validar plan contra convenciones

```markdown
ACCIÓN: Verificar adherencia a standards del proyecto

Herramientas a usar:
- read_file: Leer .github/instructions.md
- grep_search: Buscar patrones en código existente

Prompt sugerido:
"Valida el plan contra:
- Convenciones de código del proyecto (instructions.md)
- Patrones existentes en el codebase
- Estándares de seguridad
- Requisitos de testing

Ajusta el plan si es necesario."
```

### ✅ Output esperado de Fase 2:

- ✓ Plan de implementación detallado y secuencial
- ✓ Lista de TODOs en manage_todo_list
- ✓ Documentación de Context7 consultada y guardada
- ✓ Validaciones de seguridad identificadas
- ✓ Plan validado contra convenciones del proyecto

**⏸️ PAUSA AQUÍ - Cambia de modelo antes de continuar a Fase 3**

---

## 💻 FASE 3: Codificación e Implementación

**🎯 Objetivo:** Implementar el código siguiendo el plan, validando en cada paso.

**📊 Modelo recomendado:** Claude Sonnet 4.5 (excelente en codificación precisa)

**Pasos a ejecutar:**

### 3.1 Preparar entorno Git

```markdown
ACCIÓN: Crear branch para la tarea

Herramientas MCP:
- create_branch: Crear branch siguiendo convención

Prompt sugerido:
"Crea branch siguiendo la convención:
- feature/TASK-XXX-descripcion-corta
- fix/TASK-XXX-descripcion-corta
- refactor/TASK-XXX-descripcion-corta

Usa nombres descriptivos en kebab-case, max 50 chars."
```

### 3.2 Implementar código paso a paso

```markdown
ACCIÓN: Codificar siguiendo el plan de Fase 2

Herramientas a usar:
- create_file: Crear nuevos archivos
- replace_string_in_file: Editar archivos existentes
- multi_replace_string_in_file: Múltiples edits eficientes
- get_errors: Validar después de cada cambio
- manage_todo_list: Marcar progreso

Prompt sugerido:
"Implementa el plan de Fase 2:

1. Marca TODO como 'in-progress' antes de empezar
2. Implementa el código del paso actual
3. Verifica errores con get_errors
4. Si no hay errores, marca TODO como 'completed'
5. Continúa con siguiente paso

IMPORTANTE:
- Sigue exactamente las convenciones de instructions.md
- Usa type hints en todas las funciones
- Agrega docstrings cuando sea necesario
- NO hardcodees credenciales o secretos
- Valida inputs de usuarios"
```

### 3.3 Crear migraciones si es necesario

```markdown
ACCIÓN: Migraciones de base de datos (si aplica)

Herramientas a usar:
- run_in_terminal: Ejecutar comandos alembic

Prompt sugerido:
"Si modificaste modelos de BD:
1. Crea migración: alembic revision --autogenerate -m 'descripcion'
2. Revisa el archivo de migración generado
3. Aplica en dev: alembic upgrade head
4. Verifica que todo funciona"
```

### 3.4 Ejecutar tests y validaciones

```markdown
ACCIÓN: Validar implementación completa

Herramientas a usar:
- run_in_terminal: Ejecutar tests
- get_errors: Verificar errores finales

Prompt sugerido:
"Valida la implementación:
1. Ejecuta tests si existen: pytest
2. Verifica linting/typing si aplica
3. Confirma que se cumplen criterios de aceptación
4. Revisa que no hay errores con get_errors
5. Prueba manualmente la funcionalidad (si es posible)"
```

### 3.5 Crear Pull Request

```markdown
ACCIÓN: Crear PR con toda la documentación

Herramientas MCP:
- create_pull_request: Crear PR en GitHub
- notion-update-page: Actualizar estado en Notion (requiere page_id)
- notion-create-comment: Agregar link al PR (requiere page_id)

⚠️ IMPORTANTE:
- SIEMPRE usar notion-fetch primero para obtener el ID correcto de la página
- NUNCA intentar actualizar Notion usando URLs directamente
- Si notion-update-page falla, reportar el error y continuar con el PR
- Si notion-create-comment falla, informar pero no bloquear el proceso

Prompt sugerido:
"Crea Pull Request con:

TÍTULO:
[TASK-XXX] Descripción clara y concisa

DESCRIPCIÓN:
## 🎯 Tarea
Link a Notion: [URL] (solo para referencia visual, no para acceso programático)

## 📝 Descripción
[Resumen de cambios implementados]

## ✅ Criterios de Aceptación
- [ ] Criterio 1 de Notion
- [ ] Criterio 2 de Notion
- [ ] ...

## 🔧 Cambios Técnicos
- Archivo1: [Cambios]
- Archivo2: [Cambios]

## 🧪 Testing
[Cómo probar los cambios]

## 📚 Documentación Context7 Consultada
- Librería1: [Link]
- Librería2: [Link]

## 📸 Screenshots (si aplica)
[Capturas o demos]

Luego, usando el page_id obtenido de notion-fetch:
1. Usa notion-update-page para cambiar estado a 'In Review'
   - Si falla, reportar: 'Error al actualizar estado en Notion: [mensaje de error]'
2. Usa notion-create-comment para agregar link al PR
   - Si falla, reportar: 'Error al crear comentario en Notion: [mensaje de error]'
3. Confirma qué operaciones fueron exitosas y cuáles fallaron"
```

### ✅ Output esperado de Fase 3:

- ✓ Código implementado y funcionando
- ✓ Tests pasando (si existen)
- ✓ Pull Request creado con descripción completa
- ✓ Tarea en Notion actualizada a "In Review"
- ✓ Link entre GitHub PR y Notion establecido
- ✓ Sin errores de linting o typing

---

## 📖 EJEMPLO PRÁCTICO: Flujo Completo con Cambio de Modelo

### Ejemplo: "Implementar endpoint de exportación de reportes"

#### **FASE 1: Recuperación de Contexto** 🔍
**Modelo recomendado: Gemini 2.0 Flash Thinking**

```
TÚ: "Busca en Notion tareas con 'exportación' en el título que estén en estado 'To Do' 
y trae los detalles completos de la más prioritaria"

GEMINI: 
1. Usa notion-search con query "exportación status:To Do"
2. Usa notion-fetch para obtener detalles completos de la tarea más prioritaria
   - Si notion-fetch falla: "Error al acceder a Notion: [mensaje]"
3. Si todo es exitoso:
   - Encuentra: "Implementar exportación de reportes a Excel"
   - Extrae: Criterios de aceptación, especificaciones técnicas, archivos relacionados
   - Resume: "Tarea requiere endpoint FastAPI POST /reports/export con formato Excel usando openpyxl"
```

⏸️ **PAUSA AQUÍ - Cambia a Claude Opus 4.5**

---

#### **FASE 2: Planificación** 🎯
**Modelo recomendado: Claude Opus 4.5**

```
TÚ: "Usa la documentación de FastAPI y openpyxl de Context7 para crear un plan 
detallado de implementación del endpoint de exportación"

OPUS: [Usa get-library-docs con /fastapi/fastapi y /openpyxl/openpyxl]
- Consulta: Response streaming, File responses, openpyxl writer
- Propone:
  1. Nuevo archivo: app/api/routes/reports.py
  2. Schema: ReportExportRequest con filtros y formato
  3. Servicio: ExcelReportGenerator con openpyxl
  4. Endpoint: POST /reports/export retorna FileResponse
  5. Tests: test_reports.py con mock de DB
- Entregables: 5 archivos a crear/modificar, orden de implementación
```

⏸️ **PAUSA AQUÍ - Cambia a Claude Sonnet 4.5**

---

#### **FASE 3: Implementación** 💻
**Modelo recomendado: Claude Sonnet 4.5**

```
TÚ: "Implementa el plan anterior paso a paso. Primero crea el archivo routes/reports.py"

SONNET: 
1. Crea app/api/routes/reports.py con endpoint
2. Crea app/schemas/report.py con modelos Pydantic
3. Crea app/services/excel_generator.py con lógica openpyxl
4. Actualiza app/api/__init__.py para incluir router
5. Instala dependencia: pip install openpyxl
6. Ejecuta tests: pytest tests/api/test_reports.py
7. Valida con get_errors

TÚ: "Crea el PR y actualiza Notion"

SONNET: 
1. Usa create_pull_request con descripción completa
2. Usa notion-fetch para obtener el page_id de la tarea
   - Si falla: "No se pudo obtener información de Notion: [mensaje]"
3. Usa notion-update-page para cambiar Status → "In Review"
   - Si falla: "PR creado exitosamente, pero no se pudo actualizar Notion: [mensaje]"
4. Usa notion-create-comment para agregar Link → PR
   - Si falla: "PR creado pero comentario no pudo ser agregado: [mensaje]"
5. Reporta estado final: qué operaciones fueron exitosas y cuáles fallaron
```

---

### 🎯 Resultado Final del Ejemplo:

✅ **Fase 1 (Gemini):** Contexto completo recuperado en 2 min  
✅ **Fase 2 (Opus):** Plan técnico detallado en 5 min  
✅ **Fase 3 (Sonnet):** Código implementado y PR creado en 15 min  
⏱️ **Tiempo total:** ~22 minutos para tarea completa  
🔄 **Cambios de modelo:** 2 pausas manuales (entre fases)

---

---

## 🔄 Post-Implementación (Opcional - Mismo modelo de Fase 3)

### Seguimiento del PR

```markdown
Si hay comentarios de code review:
1. Revisar comentarios
2. Aplicar correcciones necesarias
3. Actualizar PR con explicación
4. Comentar en Notion si hay cambios significativos

Al hacer merge:
1. Actualizar Notion a "Done"
2. Agregar comentarios finales o lecciones aprendidas
3. Verificar que branch se cerró (si no, cerrar manualmente)
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
10. ✅ **ACTUALIZAR estado** de tareas usando notion-update-page con page_id
11. ✅ **DOCUMENTAR bloqueos** usando notion-create-comment inmediatamente
12. ✅ **AGREGAR links** entre Notion y GitHub usando notion-create-comment
13. ✅ **NUNCA acceder URLs directamente** - siempre usar herramientas MCP
14. ✅ **REPORTAR errores MCP** inmediatamente si notion-fetch, notion-update-page o notion-create-comment fallan
15. ✅ **OBTENER page_id con notion-fetch** antes de cualquier operación de actualización

### Calidad de Código
16. ✅ **VERIFICAR errores** después de cada cambio con get_errors
17. ✅ **SEGUIR convenciones** definidas en instructions.md del proyecto
18. ✅ **EJECUTAR tests** antes de crear PR (si existen)

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
- **Actualiza frecuentemente**: No esperes al final del día, usa notion-update-page regularmente
- **Sé específico**: Los comentarios vagos no ayudan al equipo
- **Marca bloqueos ASAP**: Si algo te detiene, escálalo inmediatamente con notion-create-comment
- **Siempre usa MCP**: Nunca intentes acceder URLs de Notion directamente
- **Maneja errores**: Si el MCP falla, reporta el error específico al usuario
- **Obtén page_id primero**: Usa notion-fetch antes de cualquier operación de actualización

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
❌ **NO intentar acceder URLs de Notion directamente sin MCP**
❌ **NO ignorar errores del MCP de Notion - siempre reportarlos**
❌ **NO actualizar Notion sin primero obtener el page_id con notion-fetch**

---

## 🤖 Selección de Modelos por Tarea

### Estado Actual (Diciembre 2025)

VS Code **no soporta nativamente** orquestación multi-modelo por fase de trabajo. Consulta [MULTI-MODEL-WORKFLOW.md](../MULTI-MODEL-WORKFLOW.md) para detalles completos.

**Opciones disponibles:**

1. **Manual:** Usuario cambia modelo en dropdown de Chat view por fase
2. **Un modelo potente:** Usar Claude Sonnet 4.5 o Gemini 2.0 para todo el flujo
3. **Extensión custom:** Desarrollar chat participants especializados por tarea
4. **Script externo:** Orquestación fuera de VS Code con APIs directas

### Configuración Recomendada

**Enfoque pragmático actual:**

```markdown
# Seleccionar UN modelo para toda la sesión:
- Claude Sonnet 4.5 (recomendado): Excelente en análisis, plan Y código
- Gemini 2.0 Flash Thinking: Rápido y capaz en múltiples dominios

# Estructurar prompts en fases dentro del mismo modelo:
1. Fase de análisis: "Analiza esta tarea en detalle..."
2. Fase de planificación: "Basándote en el análisis, crea plan..."
3. Fase de implementación: "Siguiendo el plan, implementa..."
```

**Si necesitas absolutamente diferentes modelos:**
- Cambia manualmente el modelo antes de cada fase
- O desarrolla extensión con chat participants especializados

---

## 📚 Referencias Útiles

- **Context7 MCP**: Para documentación actualizada de librerías
- **Notion MCP Docs**: https://developers.notion.com/docs/mcp-supported-tools
- **GitHub MCP Server**: https://github.com/github/github-mcp-server
- **GitHub MCP Toolsets**: Ver tabla completa en README del servidor oficial
- **Multi-Model Workflow**: Ver [MULTI-MODEL-WORKFLOW.md](../MULTI-MODEL-WORKFLOW.md)
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
2. notion-fetch: Obtener detalles de cada página encontrada usando su page_id
3. Analizar resultados
4. notion-create-pages: Crear página de resumen con links
5. Si algún paso falla, reportar: "Error en [herramienta MCP]: [mensaje de error]"
6. Retornar URL de la nueva página solo si todo fue exitoso
```

### Ejemplo 2: Crear feature completo con GitHub
```
Usuario: "Implementa el endpoint de login según el ticket TASK-123 en Notion"

Agente:
1. notion-search: Buscar "TASK-123" en Notion
2. notion-fetch: Obtener detalles completos usando el page_id encontrado
   - Si falla: "Error al obtener tarea de Notion: [mensaje]"
3. Context7: Buscar docs de FastAPI y Argon2
4. create_branch: feature/TASK-123-login-endpoint
5. create_or_update_file: Múltiples archivos
6. create_pull_request: Con referencia a TASK-123
7. notion-update-page: Cambiar estado a "In Review" usando page_id
   - Si falla: "Error al actualizar estado en Notion: [mensaje]"
8. notion-create-comment: Agregar link al PR
   - Si falla: "Error al crear comentario: [mensaje], pero PR fue creado exitosamente"
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
