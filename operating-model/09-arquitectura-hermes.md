# 09 — Arquitectura de la oficina sobre Hermes Agent

**Estatus:** vigente (ADR-003). Prevalece sobre los docs 01, 04 y 05 donde entren en conflicto. Todo lo citado de Hermes proviene de su documentación oficial ([docs](https://hermes-agent.nousresearch.com/docs/), [repo](https://github.com/NousResearch/hermes-agent)); lo marcado **[TBV]** (to be verified) se confirma en la instalación real antes de apoyarse en ello.

## 1. Principio revisado

El diseño original decía "estado durable, cómputo efímero" porque asumía que no había forma asequible de tener cómputo persistente. Hermes lo cambia: **el daemon es persistente y su memoria también**. El principio queda así:

- **Hermes = la oficina viva.** Daemon 24/7 en la VM: conversación continua, memoria entre sesiones, skills que crecen, cron, subagentes.
- **Git = el archivo canónico.** Lo curado, auditable y versionado (dossiers, ADRs, specs, playbooks) sigue en este repo. La memoria de Hermes es operativa/episódica; el repo es la verdad institucional. Hermes lee y escribe el repo como parte de su trabajo.
- **Claude Code = el arquitecto externo.** Diseño, construcción crítica y QA de segundo par de ojos, sobre la suscripción Claude Pro, vía PRs y sesiones. Fuera del daemon a propósito: el que audita no vive dentro de lo auditado.

## 2. Topología de la oficina

```
                         PROPIETARIO
                  Telegram (@Tartaloagentbot) · GitHub PRs
                        │ pairing DM + command approval
┌───────────────────────▼───────────────────────────────┐
│  HERMES AGENT (daemon, VM nueva, 24/7)                │
│  Rol raíz: Jefe de Gabinete (JdG)                     │
│  · gateway Telegram (aprobaciones, intake, resúmenes) │
│  · memoria nativa SQLite+FTS5 (episódica/operativa)   │
│  · skills agentskills.io (roles y procedimientos)     │
│  · cron (resumen diario, retro semanal, TTLs)         │
│  · subagentes aislados = especialistas efímeros       │
│    (Investigación ∥ Estratega ∥ Constructor ∥ QA…)    │
│  · terminal backend: Docker (sandbox por defecto)     │
└───────────┬───────────────────────────────────────────┘
            │ lee/escribe (git, gh)
┌───────────▼───────────────────────────────────────────┐
│  REPO DE GOBIERNO kaikhermes + repos de producto      │
│  knowledge/ · decisions/ · playbooks/ · skills/ ·     │
│  domains/ · GitHub Issues (tablero)                   │
└───────────▲───────────────────────────────────────────┘
            │ PRs, revisiones, diseño
   CLAUDE CODE (arquitecto/QA crítico, suscripción Pro)
```

- **El JdG es el propio Hermes raíz**: prioriza, descompone, mantiene el tablero, pide aprobaciones. Sigue sin hacer trabajo especializado: lo delega en **subagentes aislados** (primitiva nativa: "spawn isolated subagents for parallel workstreams").
- **El roster de roles del doc 01 se conserva íntegro** (mandatos, autoridad, KPIs); cambia la implementación: cada rol es una **skill semilla** en formato agentskills.io que el subagente carga al instanciarse. Los playbooks de dominio (`domains/*/playbook.md`) se cargan igual.
- **QA sigue en contexto separado**: subagente propio, sin las notas del Constructor — el aislamiento de subagentes de Hermes lo hace natural.
- **Trabajos de owner único** (arquitectura, finanzas EZTI, legal, releases): los ejecuta el JdG con nivel de modelo alto o un único subagente, nunca fragmentados — la regla del doc 01 §2 no cambia.

## 3. Memoria y conocimiento: dos niveles con frontera explícita

| Nivel | Dónde | Qué | Gobernanza |
|---|---|---|---|
| **Episódico/operativo** | Memoria nativa de Hermes (SQLite+FTS5, resúmenes LLM) | Conversaciones, contexto de trabajo, recuerdo entre sesiones | Autónoma (es la gracia de Hermes); revisión por muestreo en la retro |
| **Canónico/curado** | Este repo (git) | Hechos con fuente/fecha/TTL, ADRs, specs, playbooks, dossiers | Igual que doc 03: PR + merge según nivel; **nada canónico se escribe solo en la memoria de Hermes** |

Regla de promoción: cuando algo operativo merece ser institucional (un hecho verificado, una decisión, un procedimiento), Hermes lo escribe al repo vía PR — su memoria no sustituye al archivo, lo alimenta.

**Skills — el punto más delicado del sustrato.** Hermes crea skills autónomamente (tras tareas de 5+ tool calls) y las parchea en uso. Eso es exactamente el "autoaprendizaje sin gobernanza" que el doc 03 prohibía, así que se gobierna así:

1. Las skills auto-creadas nacen en cuarentena funcional: utilizables por el daemon, pero **la retro semanal las revisa todas** (diff contra la semana anterior) y decide: promover al repo (canonizar), corregir o borrar.
2. Toda skill que implique acción externa (publicar, contactar, gastar, desplegar) debe incluir el paso de gate R2/R3 **dentro de su procedimiento** — y esto se audita en la retro.
3. Las skills semilla de los roles y las de gobernanza viven en el repo (`skills/`) y se instalan en Hermes; la versión del repo es la canónica.
4. **[TBV]** Verificar en instalación si Hermes permite desactivar o gatear la auto-creación/parcheo de skills por configuración; si sí, evaluar activar el gate para skills que tocan acciones externas.

## 4. Gobernanza R0–R3 sobre mecanismos nativos

La política (doc 06) no cambia; cambia el mecanismo de aplicación:

| Nivel | Mecanismo en Hermes |
|---|---|
| R0/R1 (interno) | Ejecución normal del daemon/subagentes; registro en memoria + log; visible en resumen diario |
| R2/R3 (público, terceros, prod real, gasto nuevo) | **Command approval del gateway** + regla de sistema: el JdG formula la solicitud con el formato de gate (qué/por qué/rollback) y espera tu respuesta por Telegram. Silencio = pendiente, jamás timeout-approve |
| Prohibidos | Triple barrera: (a) los secretos Tier-0 **no existen** en la VM — imposibilidad material; (b) denylist de comandos/herramientas en la config de Hermes **[TBV granularidad]**; (c) prohibiciones en el prompt de sistema/playbooks — la barrera débil, por eso es la tercera y no la única |
| Kill switch | Parar el daemon (`systemctl stop hermes` o equivalente) + comando de pausa vía gateway **[TBV]**. Se documenta en el runbook y se prueba en la instalación |

- **DM pairing** del gateway: solo tu cuenta de Telegram habla con el daemon. Se configura en la instalación y se prueba con una cuenta ajena (debe rechazarla).
- **Seguridad de ejecución:** terminal backend **Docker** — los comandos del agente corren en contenedor, no directamente sobre el host. El host solo lleva el daemon, su config y los secretos Tier-1 con permisos mínimos.

## 5. Modelos: política de backends por suscripción

Verificado en la doc de providers de Hermes: OAuth de suscripción para Anthropic, OpenAI Codex (device-code), GitHub Copilot, xAI; Vertex AI vía service account. Política:

| Uso | Backend | Justificación |
|---|---|---|
| Trabajo rutinario del daemon (triaje, resúmenes, investigación estándar, borradores) | **OpenAI Codex OAuth** (tu ChatGPT Plus) | Suscripción ya pagada; reparte carga y preserva la ventana de Claude Pro para lo crítico |
| Nivel 3 del daemon (memos de decisión, QA crítico, redacción final R2+) | **Anthropic OAuth** — **[TBV]: la doc cita Claude Max + créditos extra; verificar si Pro basta.** Si Pro no basta: escalar estas tareas a Claude Code (yo) vía repo, o evaluar coste de Max con datos | Calidad máxima donde el error es caro |
| Bulk barato (digestión de documentos largos, extracción, clasificación masiva) | **Vertex AI con créditos GCP** (service account) — vía legítima, compatible con ToS | Coste real ≈0 mientras duren créditos |
| Emergencia/picos si todo lo anterior falla | OpenRouter (API key, prepago pequeño) | Sin lock-in, control de gasto fino |
| Descartado | Google AI Pro de consumo | Decisión del propietario: contra ToS. No se usa aunque sea técnicamente posible |

- **Riesgo asumido y registrado:** el uso de OAuth de suscripción en harnesses de terceros depende de las políticas de cada proveedor y puede cambiar o ser revocado. Mitigación: multi-proveedor desde el día 1 (la caída de uno no para la oficina) + OpenRouter como red de seguridad de pago.
- **Conflicto de ventana compartida:** si el daemon usa Anthropic OAuth del mismo plan Pro que mis sesiones de Claude Code, competimos por la misma cuota. Por eso el default del daemon es Codex y Anthropic se reserva a nivel 3. El ledger de tres ventanas (Claude Pro / ChatGPT Plus / créditos GCP) mide el reparto real y alimenta la decisión de plan en F2.
- `hermes model` / `/model` permiten cambiar proveedor sin tocar código; la config canónica vive en `~/.hermes/config.yaml` y se documenta (sin secretos) en `infra/`.

## 6. Clean-room aplicado a Hermes

1. Instalación **nueva** (release estable actual) en la VM nueva: `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` — nunca sobre la VM antigua.
2. `~/.hermes/` nace en blanco: **prohibido** copiar config, memoria (SQLite), skills o workspace del Hermes antiguo. Prohibido `hermes claw migrate` y cualquier importación equivalente.
3. El Hermes antiguo queda dentro de la cuarentena general de la VM antigua (runbook §1); si algún día algo mereciera rescate, regla de importación ítem a ítem con autorización escrita.
4. El bot @Tartaloagentbot es nuevo (creado 2026-07-06) → limpio; recomendación de regenerar token en el deploy sigue vigente.
5. Workspace de trabajo del daemon: `/srv/mandi/office/` (nuevo), con el repo de gobierno clonado dentro.

## 7. Qué se retira, qué se conserva

| Elemento del diseño v1 | Destino |
|---|---|
| `services/` Python (gateway, ledger, watchdog) | **Retirados** → `archive/pre-hermes-services/` (referencia/rollback; no se despliegan). Gateway → gateway nativo; cron/watchdog → cron nativo + monitorización del daemon |
| Ledger de dos (ahora tres) divisas | **Concepto se conserva.** Implementación: capacidad nativa de Hermes si existe **[TBV]**; si no, skill+cron dentro de Hermes que registra gasto/ventanas en el repo |
| Tablero GitHub Issues + `ESTADO.md` | Se conservan; los mantiene el JdG (Hermes) con `gh` |
| Gobernanza R0–R3, prohibidos, acta FASE 1 | Sin cambios |
| Roster de roles, playbooks de dominio | Sin cambios; se convierten en skills semilla |
| Pipeline INTAKE→RETRO (doc 05) | Sin cambios; INTAKE ahora entra por el gateway nativo |
| Investigación EZTI (proveedores, normativa) | Sin cambios — es conocimiento, portable |
| Precondiciones de VM (ADR-002) | Sin cambios; siguen bloqueando |
| `infra/bootstrap.sh` | Se simplifica: hardening base + preparación para `hermes` (sin servicios propios) |
| Gmail solo-lectura, secretos Tier-0/1 | Sin cambios (ADR-002) |

## 8. Plan de validación de la instalación (los [TBV], en orden)

Antes de dar la oficina por operativa, en la VM real y con registro en el issue #5:

1. **Auth:** ¿funciona Anthropic OAuth con tu plan **Pro**? (la doc cita Max). ¿Funciona Codex device-code con tu ChatGPT Plus? ¿Vertex con tu service account?
2. **Gateway:** pairing DM con tu cuenta; rechazo verificado de cuenta ajena; command approval — ¿qué granularidad real ofrece? ¿comando a comando, por categoría, allowlist?
3. **Kill switch:** cómo se pausa/para el daemon desde Telegram y desde systemd; probarlo.
4. **Skills:** ¿se puede gatear/desactivar la auto-creación o el auto-parcheo? ¿dónde viven los archivos de skill y cómo se versionan al repo?
5. **Cron:** definir resumen diario y retro semanal; verificar ejecución.
6. **Subagentes:** aislamiento real (¿comparten memoria/credenciales con el raíz?); coste por subagente en ventanas de suscripción.
7. **Gasto/uso:** ¿expone Hermes métricas de tokens/uso por proveedor? Si no → skill de ledger.
8. **Sandbox:** confirmar terminal backend Docker activo y que un comando destructivo queda confinado al contenedor.

Cada punto se marca verificado/fallido con fecha; los fallidos generan decisión (workaround, feature request, o ajuste del diseño). **Ningún gate de autonomía se relaja hasta completar esta lista.**

## 9. F0 revisado (secuencia)

1. Precondiciones de VM (#2) — sin cambios, siguen siendo tuyas.
2. VM nueva + `bootstrap.sh` (hardening base).
3. Instalar Hermes limpio + `hermes setup` + `hermes model` (Codex primero; Anthropic y Vertex después).
4. Gateway Telegram con @Tartaloagentbot (token regenerado) + pairing + prueba de rechazo.
5. Cargar skills semilla (roles, gobernanza, gates) y playbooks; clonar repo de gobierno en el workspace.
6. Plan de validación §8 completo.
7. Reanudar el Sprint 1 de EZTI **dentro de la oficina**: el JdG-Hermes toma el issue #1 con el conocimiento ya acumulado en el repo.
