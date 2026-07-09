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

- ✅ B1, B2, B3 (base, `hermes doctor` OK, Codex OAuth) — hermes-agent (Nous Research), no NousResearch/hermes-agent genérico
- ✅ B4 (Anthropic) y **V4 resuelto en SÍ**: la key visible en `hermes status` → API Keys es el token interno de validación de la sesión OAuth de tu plan Pro, no una clave de pago por token. Confirmado por el propietario 2026-07-09. Daemon usa Claude para nivel 3, sin coste incremental.
- ✅ V2/Vertex resuelto como **NO** (decisión del propietario, 2026-07-08): política de organización GCP bloquea creación de llaves de service account (`constraints/iam.disableServiceAccountKeyCreation`); en vez de reasignar el SA de la VM, se aplaza Vertex — bulk se queda en Codex, no se contrata nada nuevo. SA `hermes-vertex` creado con rol `aiplatform.user` pero sin uso (sin llave); pendiente borrado de limpieza (opcional).
- ✅ B6 confirmado por `hermes status`: gateway Telegram activo vía systemd (user).
- ⏳ B7: repo clonado en `~/office/kaikhermes` (iba en rama equivocada, corrigiendo a `claude/agent-system-next-steps-63li8s`); instalación de las 13 skills semilla vía `hermes skills install <raw-URL-SKILL.md>` en curso.
- ⏳ B8 (cron): sintaxis confirmada (`hermes cron create <schedule> <prompt> --name --skill --workdir --deliver`); 5 jobs de PLAN §4 preparados, pendiente de ejecutar en la VM (con `timedatectl` a Europe/Madrid antes).
- ⏳ B9 (sandbox): `hermes status` → Terminal Backend: **local**; `config.yaml` tiene `docker_mount_cwd_to_workspace: false` (sugiere soporte Docker existente pero inactivo); pendiente contexto de la sección y `hermes config --help` para el comando exacto de activación.
- ⏳ B10 (kill switch): mecanismo identificado (`hermes gateway {stop,start,restart,status}`), pendiente de probar.
- ⏳ B11: checklist issue #5, pendiente de todo lo anterior.

## Decisiones abiertas (PLAN §10 + nuevas de la instalación real)

GO shortlist EZTI (#1) · nombre del sistema · datos música E13 · credenciales redes EZTI · asesor alimentario · clasificar kaikuv1 · borrar openclaw-core (F2) · caducidad créditos GCP · qué es "ultracode" · **nueva: ¿confirmar/revertir la API key de pago de Anthropic (V4)?**
