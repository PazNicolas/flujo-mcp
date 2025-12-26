# Ejemplo de Tarea Optimizada para Agentes de IA

Este documento muestra el formato óptimo para escribir tareas en Notion que serán procesadas por agentes de IA.

---

## 📋 Plantilla de Tarea

Copia esta estructura en tu base de datos de Notion:

---

# TASK-001: Implementar endpoint de estadísticas de usuario

## Metadatos

| Campo | Valor |
|-------|-------|
| **ID** | TASK-001 |
| **Tipo** | Feature |
| **Prioridad** | Medium |
| **Estado** | To Do |
| **Estimación** | 2h |
| **Sprint** | Sprint 1 |
| **Asignado** | @agente |

---

## Descripción

Crear un nuevo endpoint `GET /api/users/me/stats` que retorne estadísticas del usuario autenticado.

### Contexto
Los usuarios necesitan ver un resumen de su actividad en la plataforma. Esta información será consumida por el dashboard del frontend.

### Objetivo
Proporcionar un endpoint que retorne métricas básicas del usuario como fecha de registro, último login, y cantidad de acciones realizadas.

---

## Especificación Técnica

### Endpoint
```
GET /api/users/me/stats
Authorization: Bearer <token>
```

### Response Schema
```json
{
  "user_id": 1,
  "username": "john_doe",
  "member_since": "2024-01-15T10:30:00Z",
  "last_login": "2024-12-26T08:00:00Z",
  "days_active": 345,
  "stats": {
    "total_logins": 150,
    "profile_completeness": 85
  }
}
```

### Response Codes
| Código | Descripción |
|--------|-------------|
| 200 | Estadísticas retornadas exitosamente |
| 401 | No autenticado |
| 403 | Token inválido o expirado |

---

## Archivos Afectados

```
app/api/routes/users.py          # Agregar nuevo endpoint
app/schemas/user_stats.py        # Crear nuevo schema (NUEVO)
app/models/user.py               # Posible modificación si se necesitan campos
```

---

## Criterios de Aceptación

- [ ] Endpoint responde con status 200 para usuarios autenticados
- [ ] Endpoint responde con status 401 si no hay token
- [ ] Response sigue el schema especificado
- [ ] `member_since` usa la fecha `created_at` del usuario
- [ ] `days_active` se calcula desde `created_at` hasta hoy
- [ ] El campo `profile_completeness` calcula % de campos completados (email, username, full_name)
- [ ] Documentación OpenAPI generada automáticamente
- [ ] Código sigue las convenciones del proyecto (type hints, docstrings)

---

## Dependencias

- Ninguna tarea bloqueante
- Requiere: Sistema de autenticación JWT (✅ Completado)

---

## Notas para el Agente

### Librerías a consultar en Context7
- FastAPI (response_model, dependency injection)
- Pydantic (BaseModel, computed fields)
- SQLModel (queries, select)

### Consideraciones
1. Usar el decorador `@router.get` existente en users.py
2. Reutilizar la dependencia `CurrentUser` para autenticación
3. El schema de response debe ser un Pydantic BaseModel, no SQLModel
4. Calcular `days_active` usando `datetime.utcnow() - user.created_at`

### Ejemplo de implementación esperada
```python
@router.get("/me/stats", response_model=UserStats)
def get_user_stats(current_user: CurrentUser) -> UserStats:
    """Get current user statistics."""
    # Implementación aquí
    pass
```

---

## Checklist Pre-PR

- [ ] Código implementado según especificación
- [ ] Sin errores de linting/typing
- [ ] Endpoint probado manualmente en /docs
- [ ] Schema documentado en OpenAPI
- [ ] Actualizar estado en Notion a "In Review"

---

## Links Relacionados

- [Diseño del Dashboard](link-a-figma-o-notion)
- [API Docs actuales](http://localhost:8000/docs)
- [PR anterior relacionado](#)

---

# 💡 Claves para Tareas Efectivas

## ✅ Lo que DEBE tener una tarea

1. **ID único** - Para referencia en commits y PRs
2. **Descripción clara** - Qué y por qué
3. **Especificación técnica** - Endpoint, schemas, códigos de respuesta
4. **Archivos afectados** - Reduce tiempo de búsqueda
5. **Criterios de aceptación** - Checklist verificable
6. **Notas para el agente** - Context7 libs, consideraciones

## ❌ Lo que NO debe tener

1. Descripciones vagas ("mejorar el sistema")
2. Múltiples funcionalidades en una tarea
3. Criterios subjetivos ("que se vea bien")
4. Falta de especificación técnica
5. Dependencias no documentadas

## 📐 Formato Óptimo

```markdown
# TASK-XXX: [Verbo] [Qué] [Dónde]

## Descripción
[1-2 párrafos de contexto y objetivo]

## Especificación Técnica
[Endpoint, schemas, códigos - lo más detallado posible]

## Archivos Afectados
[Lista de rutas de archivos]

## Criterios de Aceptación
[Checklist con checkboxes]

## Notas para el Agente
[Librerías Context7, consideraciones, ejemplos]
```

---

## 🔧 Propiedades de Base de Datos en Notion

### Configuración Recomendada

| Propiedad | Tipo | Opciones |
|-----------|------|----------|
| Título | Title | - |
| ID | Text | TASK-XXX |
| Tipo | Select | Feature, Bug, Hotfix, Refactor, Docs |
| Estado | Select | Backlog, To Do, In Progress, In Review, Done, Blocked |
| Prioridad | Select | Critical, High, Medium, Low |
| Estimación | Select | 30min, 1h, 2h, 4h, 8h, 16h |
| Sprint | Relation | Base de datos de Sprints |
| Asignado | Person | - |
| PR Link | URL | - |
| Branch | Text | feature/TASK-XXX-... |
| Fecha Inicio | Date | - |
| Fecha Fin | Date | - |

### Vista Kanban
Crear una vista Kanban agrupada por "Estado" para visualizar el flujo de trabajo.

### Filtros Útiles
- **Mi trabajo**: Asignado = @me AND Estado != Done
- **Sprint actual**: Sprint = "Sprint X" AND Estado != Backlog
- **Bloqueados**: Estado = Blocked
