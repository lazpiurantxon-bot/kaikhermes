# Operating Model — Oficina Agéntica (clean-room)

Diseño completo del sistema multiagente (evolución clean-room del enfoque Hermes Agent), producido en dos fases: entrevista de descubrimiento (FASE 1) y diseño de arquitectura (FASE 2).

**Estado:** FASE 2 entregada; pendiente de revisión y GO del propietario para iniciar F0 del roadmap.

## Índice

| Documento | Contenido |
|---|---|
| [`fase-1-entrevista.md`](fase-1-entrevista.md) | Entrevista de descubrimiento |
| [`fase-1-respuestas.md`](fase-1-respuestas.md) | **Acta vinculante** de respuestas y restricciones |
| [`00-resumen-ejecutivo.md`](00-resumen-ejecutivo.md) | Resumen ejecutivo y decisiones clave |
| [`01-arquitectura-topologia-agentes.md`](01-arquitectura-topologia-agentes.md) | Arquitectura objetivo, topología, roster de agentes con mandato/autoridad/KPIs |
| [`02-clean-room-aislamiento-seguridad.md`](02-clean-room-aislamiento-seguridad.md) | Clean-room verificado, workspaces, VM, secretos Tier-0/Tier-1, checkpoints |
| [`03-memoria-skills-conocimiento.md`](03-memoria-skills-conocimiento.md) | Clases de memoria, ciclo de vida de skills, anti-deriva |
| [`04-herramientas-integraciones-modelos.md`](04-herramientas-integraciones-modelos.md) | Herramientas núcleo, qué no introducir aún, routing de modelos, Fable 5 + ultracode |
| [`05-operating-model-ejecucion.md`](05-operating-model-ejecucion.md) | Pipeline INTAKE→RETRO, QA, despliegue, monitorización, carga humana |
| [`06-gobernanza-costes-rollback.md`](06-gobernanza-costes-rollback.md) | Riesgos R0–R3, aprobaciones por Telegram, ledger, circuit breakers, auditoría |
| [`07-aplicaciones-personalizadas.md`](07-aplicaciones-personalizadas.md) | 5 aplicaciones end-to-end: EZTI ×2, Hermes/Mandi, Música, Hotel |
| [`08-roadmap-riesgos-decisiones.md`](08-roadmap-riesgos-decisiones.md) | Roadmap F0–F3, riesgos, **decisiones tomadas por ti**, **preguntas abiertas** |

## Reglas permanentes de este diseño

1. **Clean-room:** nada del sistema anterior entra sin autorización escrita ítem a ítem (verificado: este repo estaba vacío al iniciar — el primer commit es un root commit).
2. **Acta:** `fase-1-respuestas.md` es el contrato de restricciones; se enmienda con fecha, no se edita en silencio.
3. **Gates:** ninguna acción R2+ (público, terceros, producción real, gasto nuevo) sin aprobación humana registrada.
