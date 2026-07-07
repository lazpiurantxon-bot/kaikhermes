# ESTADO — 2026-07-07 (actualización 6 — ADR-005 agency-agents)

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

**Act. 6 — adopción selectiva de agency-agents (ADR-005):** revisado el repo
público msitarzewski/agency-agents por encargo del propietario. Se adopta lo
útil real, nada más: (1) sus datos de integración con Hermes desatascan los
[TBV] de `office/hermes/instalacion.md` §2 (destilado en
`knowledge/core/agency-agents-hermes.md`); (2) lint determinista del
catálogo de skills (`office/tests/test_skills.py` — la suite pasa de 43 a
**74 tests en verde**; skill nueva sin clasificar acción-externa/gate rompe
la suite); (3) su plugin router como paso **opcional** post-B12
(instalacion.md §6, pineado). Rechazado: importar los ~280 agentes al
catálogo (PLAN §3 sigue cerrado), runbooks NEXUS, app y convertidores.

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
