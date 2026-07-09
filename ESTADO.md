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
- ❌ B4 (Anthropic) y **V4 resuelto en NO** (corrige la entrada anterior, que fue prematura): log real de `~/.hermes/logs/errors.log` 2026-07-09 02:09 CEST — `HTTP 400 api.anthropic.com: "Third-party apps now draw from your extra usage, not your plan limits."` El plan Pro vía OAuth de terceros (Hermes) no cubre uso gratis; requiere comprar "extra usage" aparte. **Aplicada la rama NO de PLAN §5:** nivel 3 se escala a Claude Code vía repo; no se financia "extra usage" sin pasar por ese proceso (solo reevaluar si ledger registra ≥3 escalados/semana en 2 semanas). Corregido el modelo por defecto del daemon de vuelta a OpenAI Codex (Anthropic estaba puesto como default y hacía fallar hasta un "Hola" en Telegram).
- ✅ V2/Vertex resuelto como **NO** (decisión del propietario, 2026-07-08): política de organización GCP bloquea creación de llaves de service account (`constraints/iam.disableServiceAccountKeyCreation`); en vez de reasignar el SA de la VM, se aplaza Vertex — bulk se queda en Codex, no se contrata nada nuevo. SA `hermes-vertex` creado con rol `aiplatform.user` pero sin uso (sin llave); pendiente borrado de limpieza (opcional).
- ✅ B6 confirmado por `hermes status`: gateway Telegram activo vía systemd (user).
- ⏳ B7: repo clonado en `~/office/kaikhermes` (iba en rama equivocada, corrigiendo a `claude/agent-system-next-steps-63li8s`); instalación de las 13 skills semilla vía `hermes skills install <raw-URL-SKILL.md>` en curso.
- ✅ B8 (cron) completado 2026-07-09: 5 jobs activos y verificados con `hermes cron list` (resumen-diario 08:00, ledger-diario 08:05, informe-semanal lunes 07:30, retro-semanal domingo 18:00, mantenimiento-mensual día 1 09:00), horarios ya en Europe/Madrid (+02:00) sin necesitar ajuste de timezone.
- ✅ B9 (sandbox) completado y verificado 2026-07-09: `terminal.backend` cambiado a `docker`; `hermes doctor` confirma "docker (daemon running)"; prueba de confinamiento real superada — Hermes reportó haber escrito un archivo en `/tmp`, pero el `ls` en el host de la VM falla con "No such file or directory" (la escritura quedó dentro del contenedor, sin montar el cwd, tal como esperado por `docker_mount_cwd_to_workspace: false`).
- ⏳ B7: `hermes doctor` sugiere las 13 skills ya instaladas ("Skills Hub: 13 hub-installed skill(s)"); pendiente confirmar con `hermes skills list` + rama git activa, y confirmar si `gh auth login` se completó (necesario para que Hermes escriba en el repo — issues, ESTADO.md, PRs — requisito de F0.C).
- ✅ B10 (kill switch) completado 2026-07-09: `hermes gateway stop/start/restart` probado, incluido en caliente durante el incidente de V4 (restart tras corregir el modelo por defecto); daemon sano tras el arreglo.
- ⏳ B11: checklist issue #5, pendiente de todo lo anterior.

## Decisiones abiertas (PLAN §10 + nuevas de la instalación real)

GO shortlist EZTI (#1) · nombre del sistema · datos música E13 · credenciales redes EZTI · asesor alimentario · clasificar kaikuv1 · borrar openclaw-core (F2) · caducidad créditos GCP · qué es "ultracode" · **nueva: ¿confirmar/revertir la API key de pago de Anthropic (V4)?**
