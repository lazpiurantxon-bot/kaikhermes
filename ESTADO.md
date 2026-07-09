# ESTADO — 2026-07-07 (actualización 5 — F0.B EN CURSO)

**Fase:** F0.B en ejecución (el propietario levantó la pausa y está ejecutando el quickstart en la VM) · **Pausa:** no · **Gasto real del mes:** 0 €

## La dirección está fijada: `PLAN.md`

El propietario pidió parar la ejecución incremental y fijar la dirección completa. Hecho: **`PLAN.md` (raíz del repo) es el plano maestro** — arquitectura final, catálogo cerrado de 13 skills semilla (ya escritas en `skills/semilla/`), cron, backends con árboles de decisión pre-resueltos, secuencia F0.B→F3 con criterios de salida, operación en régimen, presupuesto y la lista cerrada de las 10 decisiones que quedan en manos del propietario.

**Cómo retomar en cualquier sesión:** leer `PLAN.md` → este archivo → issue del paso activo.

## Hito de infraestructura (ya real)

- VM **`hermes-core`** creada y corriendo (e2-small, Ubuntu 24.04, Madrid, 34.175.116.122). Limpia: aún sin Hermes.
- `comfy-models` borrado (~28 €/mes recuperados). `openclaw-core` se queda de momento (decisión propietario). `kaikuv1` intacto, sin clasificar.
- Bot @Tartaloagentbot creado; token pendiente de regenerar en el deploy.

## Punto exacto de ejecución (F0.B — PLAN §6)

- ✅ B1-B3: base, `hermes doctor` OK, Codex OAuth como default (confirmado sano; 335k tokens del período son 100% Codex).
- ❌ B4/V4 → **NO**: `api.anthropic.com` HTTP 400 "Third-party apps now draw from your extra usage, not your plan limits" (log 2026-07-09 02:09 CEST). Nivel 3 se escala a Claude Code vía repo. Corregido el default del daemon de vuelta a Codex.
- ❌ B5/V2 → **NO** (aplazado, decisión propietario 2026-07-08): política de organización GCP bloquea `iam.disableServiceAccountKeyCreation`. Bulk se queda en Codex. SA `hermes-vertex` creado con rol `aiplatform.user` pero sin uso (limpieza opcional pendiente).
- ✅ B6: gateway Telegram activo vía systemd (user), pairing DM funcionando.
- ✅ B7: repo en `claude/agent-system-next-steps-63li8s`, 13 skills semilla instaladas (`hermes skills list`, categoría "oficina"), `gh auth` confirmado como `lazpiurantxon-bot` con scope `repo`.
- ✅ B8: 5 cron jobs activos y verificados, horarios correctos en Europe/Madrid.
- ✅ B9: sandbox Docker activo, prueba de confinamiento real superada (escritura en `/tmp` invisible desde el host).
- ✅ B10: kill switch (`hermes gateway stop/start/restart`) probado en caliente.
- ⏳ B11: checklist de validación doc09 §8 — estado por punto:
  1. Auth: Codex ✓ · Anthropic ✗ (NO, ver B4) · Vertex aplazado (ver B5)
  2. Gateway: pairing ✓ · rechazo de cuenta ajena **sin probar** (necesita una segunda cuenta real, no bloqueante) · command approval granular → NO (solo hay prompt TTY interactivo, no aplica al daemon vía gateway; compensación ya vigente: gates solo por `jdg-gate` + sandbox Docker)
  3. Kill switch ✓ (B10)
  4. Skills auto-creación: gate nativo → NO (`skills.creation_nudge_interval` es solo un recordatorio); único control = cuarentena semanal de `retro-semanal`
  5. Cron ✓ (B8)
  6. Subagentes: aislamiento real **sin verificar** — pendiente de la primera delegación real
  7. Gasto/uso: `hermes insights` da métricas nativas reales → **V5 = SÍ**; `ledger` agrega sobre esto
  8. Sandbox ✓ (B9)
  - **Pendiente crítico, es el criterio de salida real de F0.B (PLAN §6):** prueba end-to-end de un gate — el daemon propone algo R2+ por Telegram, el propietario responde `APRUEBO`, se ejecuta y queda trazado en un issue. Aún no se ha hecho.

## Decisiones abiertas (PLAN §10 + nuevas de la instalación real)

GO shortlist EZTI (#1) · nombre del sistema · datos música E13 · credenciales redes EZTI · asesor alimentario · clasificar kaikuv1 · borrar openclaw-core (F2) · caducidad créditos GCP · qué es "ultracode".
