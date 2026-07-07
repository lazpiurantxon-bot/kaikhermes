# ADR-005 — Adopción selectiva de agency-agents (roster externo de especialistas)

- **Fecha:** 2026-07-07
- **Estado:** aceptada (encargo del propietario: "implementa todo lo que nos
  sea útil de verdad; si nada aporta, no añadas nada")
- **Nivel:** R1 — no amplía autoridad delegada ni cambia arquitectura: docs,
  tests y un paso de instalación **opcional**. El PLAN y su catálogo cerrado
  de skills (§3) quedan intactos.

## Contexto

El propietario pidió revisar el repo público
[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
(MIT, ~280 especialistas-prompt en 21 divisiones + instaladores
multi-herramienta, incluido Hermes) y adoptar solo lo que aporte mejora
real. La restricción dura es nuestra propia regla: el catálogo de skills es
cerrado (PLAN §3, reafirmado en ADR-004) y todo crecimiento pasa por el
ciclo gobernado (retro → proposed → QA → merge humano).

## Decisión

Se adoptan tres cosas; se rechaza el resto.

1. **Hechos de integración con Hermes** (mejora inmediata, coste cero).
   Su código de instalación codifica mecánica real de Hermes que nosotros
   teníamos como [TBV]: `${HERMES_HOME:-~/.hermes}`, `config.yaml`,
   `plugins/` + `plugins.enabled:`, formato de plugin, y la clave
   `skills.external_dirs` para catálogos de skills externos. Destilado con
   fuente/fecha/confianza en `knowledge/core/agency-agents-hermes.md`;
   `office/hermes/instalacion.md` §2 pasa de conjetura a candidatos
   concretos a confirmar en B7.

2. **Lint determinista del catálogo de skills** (adaptación de su CI
   `lint-agents.sh`, implementación propia stdlib en
   `office/tests/test_skills.py`). Hace ejecutable la regla dura de
   `skills/README.md` — toda skill con acción externa lleva gate embebido —
   mediante clasificación fail-closed: una skill nueva sin clasificar rompe
   la suite. Esto da a la retro semanal (skill 10) un control mecánico
   además del muestreo.

3. **Plugin `agency-agents-router` como paso OPCIONAL post-B12**
   (`office/hermes/instalacion.md` §6). Es su patrón bueno: 4 tools que
   buscan/cargan especialistas bajo demanda desde disco, sin inflar el
   catálogo de skills. Los departamentos ganan una biblioteca de método
   (marketing, pricing, brand, testing…) como **contexto puntual por
   tarea**. No condiciona F0: si no se instala, nada lo echa de menos.

**Rechazado explícitamente** (sería ruido, no mejora):

- Importar personas al catálogo de skills o vendorizar los .md en este repo
  — viola PLAN §3; nuestras 19 skills están más ajustadas (CLI `oficina`,
  política de marcas, gates, castellano) que cualquier persona genérica.
- Sus runbooks/doctrina NEXUS de orquestación — redundantes con
  `orquestador-despacho` + tablero determinista (ADR-004).
- Su app de escritorio y los convertidores para otras herramientas —
  irrelevantes para una oficina que vive en un daemon.

## Consecuencias

- `office/hermes/instalacion.md`: §2 concretado (external_dirs como
  preferente, symlinks como fallback) y §6 nuevo (router opcional, pineado
  al commit `71394d8`, con reglas de uso y rollback).
- Suite de office: 43 → 74 tests (31 de lint de skills). Añadir una skill
  ahora exige declararla con/sin acción externa en el mismo PR.
- Si el router se instala y un departamento lo usa, la retro debe vigilar
  lo mismo que ya vigila: que ninguna acción externa esquive
  `oficina politica check` — el especialista cargado es contexto, no
  autoridad.
- Riesgo aceptado: los hechos de Hermes vienen de código de terceros
  (confianza media). Mitigación: siguen marcados para confirmar en B7/B12 y
  anotarse en el issue #5; el fallback por symlink se mantiene escrito.
