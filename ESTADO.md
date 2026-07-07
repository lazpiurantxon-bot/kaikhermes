# ESTADO — 2026-07-07 (actualización 5 — OFICINA AUTÓNOMA)

**Fase:** diseño e implementación de la oficina autónoma completados (ADR-004); pendiente de despliegue en la VM · **Pausa:** no · **Gasto real del mes:** 0 €

## Qué hay nuevo

Por mandato del propietario, la oficina queda completada como **oficina
autónoma de departamentos sobre Hermes Agent** (nada de scripts a medida como
sustrato: la agencia corre en el daemon — skills + cron nativo + subagentes
aislados):

- **Orquestador** (agente raíz, `skills/oficina/orquestador-despacho`): todo
  input del propietario pasa por él; tría, delega, despacha, lanza pulsos.
- **4 departamentos proactivos** (subagentes aislados): `mercado`,
  `producto`, `marketing`, `marca` — generan trabajo sin que nadie lo pida.
- **Frontera de marcas** (enmienda E1 del acta, determinista y fail-closed):
  marcas existentes (EZTI, música, hotel, hermes-core) = solo propuesta+gate
  (o prohibido); **marcas nuevas de oficina = operación autónoma con
  compliance**; terceros reales = R3 siempre.
- **Tablero + CLI `oficina`** (`office/`, stdlib puro): estados, WIP,
  breakers, gates, ledger, feed. **43 tests en verde.**
- **Panel web del propietario** (`office/panel`, 127.0.0.1:8787 vía túnel
  SSH): intake al orquestador, kanban, agentes en trabajo, gates
  APRUEBO/RECHAZO, pausas/pulso por departamento, kill switch, marcas,
  presupuesto, feed.

Documentos: `operating-model/10-oficina-autonoma.md` (diseño) ·
`decisions/ADR-004` · enmienda E1 en `fase-1-respuestas.md` · PLAN v1.1.

## Cómo retomar

Leer `PLAN.md` → este archivo → `operating-model/10-oficina-autonoma.md`.

## Punto exacto

Siguiente paso físico: **F0.B en la VM** (`infra/quickstart-f0.md`) y al
llegar a B7/B12, desplegar la oficina: `bash office/deploy.sh` +
`office/hermes/instalacion.md` (skills, prompt del raíz, cron de despacho;
los [TBV] de la versión de Hermes se verifican ahí y se anotan en el issue #5).

## Decisiones abiertas (PLAN §10, sin cambios)

GO shortlist EZTI (#1) · ejecutar F0.B · nombre del sistema · datos música
E13 · credenciales redes EZTI · asesor alimentario · clasificar kaikuv1 ·
borrar openclaw-core (F2) · caducidad créditos GCP · qué es "ultracode".
