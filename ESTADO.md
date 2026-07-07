# ESTADO — 2026-07-07 (actualización 5 — F0.B EN CURSO)

**Fase:** F0.B en ejecución (el propietario levantó la pausa y está ejecutando el quickstart en la VM) · **Pausa:** no · **Gasto real del mes:** 0 €

## La dirección está fijada: `PLAN.md`

El propietario pidió parar la ejecución incremental y fijar la dirección completa. Hecho: **`PLAN.md` (raíz del repo) es el plano maestro** — arquitectura final, catálogo cerrado de 13 skills semilla (ya escritas en `skills/semilla/`), cron, backends con árboles de decisión pre-resueltos, secuencia F0.B→F3 con criterios de salida, operación en régimen, presupuesto y la lista cerrada de las 10 decisiones que quedan en manos del propietario.

**Cómo retomar en cualquier sesión:** leer `PLAN.md` → este archivo → issue del paso activo.

## Hito de infraestructura (ya real)

- VM **`hermes-core`** creada y corriendo (e2-small, Ubuntu 24.04, Madrid, 34.175.116.122). Limpia: aún sin Hermes.
- `comfy-models` borrado (~28 €/mes recuperados). `openclaw-core` se queda de momento (decisión propietario). `kaikuv1` intacto, sin clasificar.
- Bot @Tartaloagentbot creado; token pendiente de regenerar en el deploy.

## Punto exacto de ejecución (F0.B — quickstart-f0.md)

- ✅ Paso 1 (herramientas base: curl, git) — 2026-07-07
- ⏳ Paso 2 (instalar Hermes clean-room) — siguiente
- Pendientes: Paso 3 (doctor) · Paso 4 (backends: Codex/Anthropic→V4/Vertex→V2) · Paso 5 (gateway Telegram, token por regenerar) · Paso 6 (validación, issue #5) · B7-B11 del PLAN (skills, cron, sandbox, kill switch)

## Decisiones abiertas (solo estas — PLAN §10; la #2 «ejecutar F0.B» ya está tomada: en curso)

GO shortlist EZTI (#1) · nombre del sistema · datos música E13 · credenciales redes EZTI · asesor alimentario · clasificar kaikuv1 · borrar openclaw-core (F2) · caducidad créditos GCP · qué es "ultracode".
