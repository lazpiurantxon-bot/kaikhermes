# 05 — Operating model: de idea a producto funcionando

## 1. Pipeline de estados

Toda iniciativa (idea de negocio, feature, experimento, dossier) recorre el mismo pipeline. Se representa como **GitHub Issue** con labels de dominio (`ezti`, `core`, `musica`, `hotel`…), estado y riesgo. El issue es el hilo de trazabilidad; los artefactos viven en el repo y se enlazan desde él.

```
INTAKE → TRIAGE → BRIEF → SPEC → PLAN → BUILD → QA → GATE → DEPLOY → OPERATE → RETRO
```

| Estado | Owner | Artefacto de salida | Criterio de salida |
|---|---|---|---|
| **INTAKE** | gateway (determinista) | Issue creado con el texto original | Capturado con fecha y dominio tentativo |
| **TRIAGE** | JdG | Clasificación: dominio, riesgo R0–R3, prioridad, ¿duplicado? | Decisión: avanzar / archivar / preguntar al humano |
| **BRIEF** | Analista de Investigación | Brief de validación: mercado, competidores, esfuerzo estimado, **kill-criteria** | Preguntas críticas respondidas con fuentes |
| **SPEC** | Estratega de Producto | Spec con criterios de aceptación verificables + memo go/no-go (≤3 opciones, 1 recomendada) | **Tu GO explícito** para todo lo que consuma >presupuesto de experimento o sea R2+; GO del JdG para lo menor |
| **PLAN** | JdG | Descomposición en tareas (sub-issues), asignación de roles, presupuesto | Cada tarea tiene owner, entrada y salida definidas |
| **BUILD** | Constructor | Branch `mandi/<dominio>-<slug>` con implementación + tests + notas | Autochecklist del Constructor completo |
| **QA** | Revisor QA (contexto separado) | Veredicto con evidencia de **ejecución** (no solo lectura) contra los criterios de aceptación | Aprobado, o bloqueado con lista concreta |
| **GATE** | Humano (solo R2+) | Aprobación por Telegram o PR review | `APRUEBO <id>` registrado; adjunto: checkpoint de rollback |
| **DEPLOY** | Operador SRE | Servicio desplegado + healthcheck + entrada en runbook | Healthcheck verde; rollback probado en staging al menos una vez por tipo de deploy |
| **OPERATE** | watchdog + SRE | Monitorización, alertas, correcciones R0/R1 | Estable N días según tipo |
| **RETRO** | Agente Retro (semanal) | Qué funcionó/falló, propuestas de skill/proceso como PRs | Iniciativa cerrada; `work/` destilado a `knowledge/` |

Reglas transversales:
- **Handoffs = artefactos, no conversaciones.** Un rol entrega cuando su artefacto está escrito y enlazado en el issue. Si no está escrito, no está hecho.
- **Los criterios de aceptación se escriben en SPEC y se congelan.** Cambiarlos durante BUILD exige volver a SPEC (barato al principio, carísimo después — por eso se hace así).
- **WIP limit: 2 iniciativas activas** (en BUILD/QA/DEPLOY) al inicio. La cola de SPECs aprobadas puede crecer; el trabajo en curso no.
- Las iniciativas muertas se archivan con una línea de motivo. Matar pronto es un resultado positivo y así se mide (KPI del Estratega).

## 2. Cómo se representa el backlog

- **Backlog** = issues en TRIAGE/BRIEF ordenados por prioridad del JdG (que tú puedes reordenar comentando o por Telegram).
- **Specs** = `domains/<dominio>/specs/<slug>.md` enlazadas desde el issue.
- **Tareas** = sub-issues con checkbox; visibles de un vistazo en el issue madre.
- **Entregables** = PRs (código/docs) o deploys enlazados.
- **ESTADO.md** en la raíz del repo de gobierno, regenerado en cada resumen diario: qué hay en cada estado, qué espera tu aprobación, qué se ha gastado. Es tu vista de 30 segundos sin abrir Issues.

## 3. QA y revisión

- QA **ejecuta**: corre tests, levanta el servicio, prueba los criterios uno a uno. "El código parece correcto" no es un veredicto válido.
- QA recibe spec + branch, **no** las notas del Constructor — revisión con ojos limpios, mismo principio que el clean-room.
- Para piezas no-código (dossiers, textos públicos, análisis legales): QA = verificación de fuentes (¿la cita primaria dice eso?), checklist de compliance del dominio (p. ej. claims alimentarios) y detección de afirmaciones sin respaldo.
- Doble firma para lo público: QA aprueba calidad → tú apruebas publicación (GATE). Ninguna de las dos firmas sustituye a la otra.

## 4. Despliegue

| Tipo | Destino | Autonomía |
|---|---|---|
| Web estática / marketing | Cloudflare Pages — **staging/preview** | R1: autónomo |
| Web estática — **dominio público** (`ezti.net`) | Cloudflare Pages producción | R2: gate humano |
| Servicios internos (dashboards, herramientas propias) | VM, Docker, puerto interno tras auth básica | R1: autónomo |
| Servicios con usuarios/clientes reales | Donde corresponda | R3: gate + autorización por servicio (H22) |

Todo deploy es por versión etiquetada y con procedimiento de rollback escrito en el runbook **antes** del primer deploy real de ese tipo.

## 5. Monitorización e iteración post-lanzamiento

- **Watchdog (determinista):** healthchecks HTTP por servicio, disco/CPU de la VM, éxito de backups. Fallo → alerta Telegram con severidad.
- **Métricas de producto:** para la web de EZTI, analytics de Cloudflare (sin cookies de terceros, coherente con RGPD) como línea base; ampliar solo si una decisión concreta necesita más datos.
- **Iteración:** OPERATE alimenta RETRO; la retro convierte señales (errores, fricción, métricas) en nuevos issues de INTAKE. El ciclo se cierra sin que tú tengas que empujarlo: tu papel queda en los GATEs, el reordenado de prioridades y las decisiones de los memos.

## 6. Tu carga de trabajo prevista (diseño anti-microgestión)

- **Diaria (≤5 min):** leer resumen breve de Telegram; aprobar/rechazar cola de GATEs pendientes (cada ítem con contexto de 3 líneas + enlace + rollback adjunto).
- **2–3 × semana (15–30 min):** resumen profundo: avance por línea, gasto, decisiones tomadas R0/R1, memos que esperan tu GO.
- **Semanal (opcional):** leer la retro; vetar o aprobar PRs de skills/playbooks.

Si un día no respondes, nada se rompe: lo R0/R1 sigue, lo R2+ espera en cola. El sistema nunca interpreta silencio como aprobación.
