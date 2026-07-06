# 01 — Arquitectura objetivo, topología y roster de agentes

## 1. Principio rector: estado durable, cómputo efímero

La restricción dominante es real y medible: el acceso a modelos es una **suscripción Claude Pro** con ventanas de uso limitadas, no un presupuesto API. Por tanto, la "oficina de trabajadores 24/7" no puede ser (ni necesita ser) una flota de procesos LLM permanentes. Se implementa así:

- **La continuidad de la oficina vive en el estado, no en los procesos.** Specs, decisiones, conocimiento, tablero de tareas y logs viven en git y GitHub Issues. Cualquier sesión de agente puede morir en cualquier momento sin perder nada: al arrancar, hidrata desde el estado; al terminar, escribe estado de vuelta.
- **Los agentes son sesiones acotadas de Claude Code** (interactivas contigo, o programadas vía Routines de Claude Code en la web — mecanismo verificado: esta misma sesión corre sobre esa infraestructura). Cada sesión entra con un rol, un playbook y un objetivo de salida definidos.
- **La capa 24/7 es código determinista sin LLM** en la VM: gateway de Telegram, scheduler, ledger de gasto/acciones, watchdog de salud y backups. Barato, auditable y sin consumir capacidad de modelo.

Consecuencia: "departamento" = rol + playbook + espacio de estado, no proceso. Esto es más robusto (sin drift de procesos zombis), más barato (capacidad premium solo cuando hay trabajo) y más auditable (todo pasa por git/Issues).

## 2. Topología elegida: híbrido jerárquico ligero

**Decisión:** un orquestador + especialistas efímeros por encargo + tablero durable como columna vertebral + dos roles transversales de cadencia fija.

**Por qué esta y no otras:**

| Alternativa | Veredicto | Razón |
|---|---|---|
| Manager de managers (jerarquía profunda) | Rechazada | Con 1 humano y 2 pilotos, cada capa intermedia añade latencia, coste y pérdida de contexto sin paralelización real que lo justifique. |
| Swarm / board puro sin ownership | Rechazada | Sin owner único por iniciativa no hay responsabilidad trazable; viola tu requisito de trazabilidad y QA. |
| Monolito (un solo agente para todo) | Rechazada | Contamina contexto entre dominios (EZTI ↔ música ↔ hotel), mezcla niveles de riesgo y satura la ventana de contexto. |
| Manager-especialistas plano | Base adoptada | Paralelización real solo donde existe (investigación, construcción vs QA), separación de responsabilidades clara. |
| + Tablero durable (Issues) | Añadido | Da persistencia entre sesiones y te da interfaz de revisión sin microgestión. |

**Dónde hay multiagente de verdad y dónde no:**
- **Sí** (paralelización o separación de responsabilidades real): investigación en abanico (varios frentes de búsqueda), Constructor ∥ preparación de QA, líneas de dominio independientes (EZTI avanza mientras Hermes-core itera).
- **No** (owner único obligatorio, secuencial o crítico): decisiones de arquitectura, modelado de costes/finanzas de EZTI, análisis legal/compliance, releases a producción, redacción final de cualquier pieza pública. Fragmentar esto diluye responsabilidad sin ganar velocidad.
- **El orquestador no ejecuta trabajo especializado.** Excepciones justificadas: glue trivial (<5 min), triaje que requiere leer un archivo, y rollback de emergencia cuando esperar a un SRE efímero costaría más que actuar.

## 3. Roster de agentes

Convención: **Permanente** = rol siempre definido con estado propio y cadencia; **Efímero** = se instancia por encargo con contexto limpio y muere al entregar. Todos operan bajo los niveles de riesgo R0–R3 (doc 06).

| # | Agente | Tipo | Mandato | Autoridad (puede sin permiso) | Inputs | Outputs | KPIs |
|---|---|---|---|---|---|---|---|
| 1 | **Orquestador / Jefe de Gabinete (JdG)** | Permanente (rol) | Priorizar, descomponer, enrutar, mantener el tablero coherente, preparar resúmenes y colas de aprobación | Crear/editar issues y branches; instanciar especialistas; asignar presupuesto dentro de límites; solicitar aprobaciones | Tablero, intake de Telegram, acta FASE 1, resúmenes de especialistas | Tareas asignadas, cola de aprobaciones, resumen diario/semanal | Lead time intake→asignación <24h; 0 acciones R2+ sin gate; tablero sin issues huérfanos |
| 2 | **Analista de Investigación** | Efímero | Investigar con fuentes citadas, fecha y nivel de confianza; nunca opinar sin evidencia | Búsqueda/lectura web; escribir en `work/` y proponer a `knowledge/` | Brief de investigación con preguntas concretas | Informe con fuentes primarias, confianza por afirmación, huecos declarados | % afirmaciones con fuente primaria; huecos declarados vs descubiertos después |
| 3 | **Estratega de Producto** | Efímero | Convertir investigación en specs decidibles: caso de negocio, criterios de aceptación, kill-criteria, opciones con recomendación | Redactar specs y memos go/no-go | Informes de investigación, restricciones del acta | Spec con criterios de aceptación verificables + memo de decisión con ≤3 opciones | % specs aceptadas sin retrabajo mayor; calidad de kill-criteria (ideas muertas a tiempo) |
| 4 | **Ingeniero Constructor** | Efímero por iniciativa | Implementar la spec en worktree/branch propio, con tests | Escribir código, tests, docs técnicos en su branch; desplegar a entorno interno (R1) | Spec aprobada, playbook de stack | Branch con implementación + tests + notas de release | Criterios de aceptación cumplidos al primer QA; cobertura de tests en rutas críticas |
| 5 | **Revisor QA** | Efímero, contexto SIEMPRE separado del Constructor | Verificación adversarial contra criterios de aceptación; ejecutar, no solo leer | **Bloquear merge**; exigir cambios | Branch del Constructor + spec (no las notas privadas del Constructor) | Veredicto aprobado/bloqueado con evidencia de ejecución | Defectos que escapan a producción interna; falsos bloqueos |
| 6 | **Operador SRE** | Efímero + checks programados deterministas | Desplegar, monitorizar, hacer rollback; mantener bootstrap de infra versionado | Deploy interno; rollback inmediato de cualquier cosa; deploy a prod **solo tras gate** | Release aprobada, runbooks | Servicio desplegado + healthcheck + entrada en runbook | Uptime de servicios internos; MTTR; despliegues con rollback probado |
| 7 | **Documentalista / Archivero** | Efímero post-hito | Destilar trabajo terminado a `knowledge/` y ADRs; comprimir, no acumular; mantener índices | Proponer PRs a `knowledge/` y `decisions/` | Artefactos de iniciativas cerradas | ADRs, dossiers actualizados, índice al día | KB navegable (todo a ≤2 saltos del índice); 0 conocimiento sin fuente/fecha |
| 8 | **Contralor de Gasto y Gobernanza** | Permanente (código determinista + auditoría LLM semanal) | Ledger de gasto real (€) y de capacidad de suscripción (rate-limits); clasificación de riesgo; circuit breakers | Bloquear automáticamente acciones que exceden límites | Eventos de gasto, log de acciones | Ledger, alertas, informe semanal de coste | 0 sobrepasos de límite; precisión del forecast mensual |
| 9 | **Agente Retro / Mejora Continua** | Programado semanal | Leer outcomes y logs de la semana; proponer mejoras de proceso y skills **como PRs**, nunca automergear | Abrir PRs de propuesta | Logs, tablero, incidencias | PR de mejoras + informe retro | Propuestas aceptadas/rechazadas; incidencias repetidas (debe tender a 0) |

### Líneas de dominio

Las líneas (EZTI, Hermes-core, Música, Hotel, futuras: Hogar, Deportes) **no son agentes**: son espacios de estado (`domains/<dominio>/` en el repo de gobierno + repos de producto propios) con un playbook de dominio que fija límites legales, tono, idiomas y objetivos. Cualquier especialista instanciado para una línea carga su playbook. Añadir un dominio nuevo = crear carpeta + playbook + label en Issues; no requiere tocar la arquitectura (requisito H23 cumplido por construcción).

### Reglas de instanciación

1. Un especialista efímero recibe: rol, playbook de dominio, objetivo de salida, presupuesto (tiempo/€) y **solo** los artefactos de entrada declarados. Nunca hereda la conversación completa del JdG — eso evita contaminación de contexto y mantiene los encargos auditables.
2. QA nunca comparte sesión ni notas privadas con el Constructor cuya obra revisa.
3. Máximo **2 iniciativas activas en paralelo** al inicio (WIP limit). Se amplía solo con datos de capacidad (doc 06).
4. Todo agente escribe su resultado en el artefacto correspondiente (issue, PR, doc) antes de morir; lo que no queda escrito no existió.

## 4. Vista de despliegue

```
┌─ Claude Code (suscripción Pro) ────────────────────────────┐
│  Sesiones interactivas (tú + JdG)                          │
│  Sesiones programadas (Routines) → especialistas efímeros  │
└──────────────┬─────────────────────────────────────────────┘
               │ lee/escribe
┌──────────────▼─────────────────────────────────────────────┐
│  ESTADO DURABLE                                            │
│  · kaikhermes (repo gobierno): docs, playbooks, skills,    │
│    knowledge/, decisions/, domains/                        │
│  · GitHub Issues: tablero de iniciativas y tareas          │
│  · Repos de producto: ezti-web, prototipos…                │
└──────────────┬─────────────────────────────────────────────┘
               │ sincroniza / notifica
┌──────────────▼─────────────────────────────────────────────┐
│  VM NUEVA (GCP, 24/7, SIN LLM)                             │
│  · gateway-telegram: intake, aprobaciones, alertas         │
│  · ledger: gasto real + consumo de suscripción (SQLite)    │
│  · watchdog: healthchecks, backups a GCS, disco            │
│  · servicios desplegados internos (Docker)                 │
└────────────────────────────────────────────────────────────┘
   Despliegues estáticos públicos: Cloudflare Pages (ezti.net)
```
