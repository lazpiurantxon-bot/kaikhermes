# ESTADO — 2026-07-06 (actualización 4 — PLANO MAESTRO)

**Fase:** diseño completo cerrado; implementación pausada por decisión del propietario hasta nueva orden · **Pausa:** no · **Gasto real del mes:** 0 €

## La dirección está fijada: `PLAN.md`

El propietario pidió parar la ejecución incremental y fijar la dirección completa. Hecho: **`PLAN.md` (raíz del repo) es el plano maestro** — arquitectura final, catálogo cerrado de 13 skills semilla (ya escritas en `skills/semilla/`), cron, backends con árboles de decisión pre-resueltos, secuencia F0.B→F3 con criterios de salida, operación en régimen, presupuesto y la lista cerrada de las 10 decisiones que quedan en manos del propietario.

**Cómo retomar en cualquier sesión:** leer `PLAN.md` → este archivo → issue del paso activo.

## Hito de infraestructura (ya real)

- VM **`hermes-core`** creada y corriendo (e2-small, Ubuntu 24.04, Madrid, 34.175.116.122). Limpia: aún sin Hermes.
- `comfy-models` borrado (~28 €/mes recuperados). `openclaw-core` se queda de momento (decisión propietario). `kaikuv1` intacto, sin clasificar.
- Bot @Tartaloagentbot creado; token pendiente de regenerar en el deploy.

## Punto exacto de pausa

Siguiente paso físico cuando el propietario decida: **F0.B del PLAN** (instalar Hermes en `hermes-core`, comandos en `infra/quickstart-f0.md`). Nada más que decidir: el plan ya contiene las ramas para todas las incógnitas.

## Decisiones abiertas (solo estas — PLAN §10)

GO shortlist EZTI (#1) · ejecutar F0.B · nombre del sistema · datos música E13 · credenciales redes EZTI · asesor alimentario · clasificar kaikuv1 · borrar openclaw-core (F2) · caducidad créditos GCP · qué es "ultracode".
