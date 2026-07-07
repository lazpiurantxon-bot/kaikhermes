# ADR-004 — Oficina autónoma de departamentos sobre Hermes Agent

- **Fecha:** 2026-07-07
- **Estado:** aceptada (mandato directo del propietario en sesión)
- **Nivel:** R2 (amplía la autoridad delegada y añade una capa de arquitectura) — registrada además como **enmienda E1 del acta** (`operating-model/fase-1-respuestas.md`)

## Contexto

El propietario encargó cerrar el diseño de Hermes como **oficina de agentes
autónoma de verdad**: un orquestador, departamentos especialistas que
adelanten trabajo proactivamente (desarrollo de producto, campañas de
marketing, propuestas de rebranding, análisis de mercado), y una interfaz
propia para orquestar, supervisar y usar el sistema — no solo leerlo. Con dos
reglas de marca explícitas: la oficina **no publica nada en nombre de sus
marcas existentes** ni afecta proyectos en desarrollo, pero **sí puede crear
marcas nuevas y publicar en nombre de ellas**. El propietario recalcó que el
sustrato es el **software Hermes Agent de Nous Research** (ADR-003), no un
sistema de scripts a medida.

## Decisión

1. **La oficina corre íntegramente en Hermes Agent.** El orquestador es el
   agente raíz (JdG) con la skill `orquestador-despacho`; los departamentos
   son **subagentes aislados** (primitiva nativa) instanciados con las skills
   `dep-mercado`, `dep-producto`, `dep-marketing`, `dep-marca`; la
   proactividad la dispara el **cron nativo** del daemon (un único job de
   despacho cada 15 min; las cadencias por departamento son datos del
   tablero, no jobs). Catálogo nuevo en `skills/oficina/` (las 13 semilla
   siguen vigentes y son usadas por los departamentos como procedimientos).
2. **Tablero determinista compartido** en `~/office/state` (archivos JSON),
   operado por el CLI `oficina` (stdlib, `office/bin/oficina`). Implementa lo
   que el doc 06 §4 ya exigía como código determinista: estados y
   transiciones, WIP, circuit breakers (3 fallos → pausa de departamento;
   80% de presupuesto → freeze de gasto), gates R2/R3, ledger de € y feed de
   eventos. No sustituye al tablero institucional (issues/git): lo operativo
   vive en el tablero, lo institucional se sigue promoviendo a git vía PR.
3. **Política de marcas determinista y fail-closed** (`office/core/policy.py`
   + registro `marcas.json`): protegida → como mucho propuesta+gate (o deny
   si prohibida: música, hotel); **de oficina → publicación autónoma R1 con
   compliance embebido y registro**; terceros reales → gate R3 siempre; marca
   sin registrar → protegida. Es la barrera intermedia del doc 09 §4; la
   material sigue siendo que las credenciales de marcas protegidas no existen
   en la VM, y las marcas de oficina usan credenciales propias segregadas.
4. **Panel del propietario** (`office/panel/`): FastAPI + UI estática servida
   en `127.0.0.1:8787` (acceso por túnel SSH), como **servicio systemd de
   usuario** separado del daemon. Es interfaz, no agencia: intake al
   orquestador, kanban por departamento, agentes en trabajo, gates
   APRUEBO/RECHAZO, pausas/pulso por departamento, kill switch, presupuesto,
   registro de marcas y feed. Escribe el tablero por el mismo camino que el
   CLI de los agentes.
5. **Autoridad delegada ampliada** según la enmienda E1: trabajo proactivo
   sin encargo (h) y marcas nuevas de oficina con publicación autónoma (i).
   Sin cambios: gates para todo lo que toque marcas existentes, contacto R3,
   límites de gasto, prohibidos.

## Consecuencias

- `PLAN.md` §3 ("13 skills, ni una más en F0-F1") queda enmendado: se añaden
  las 6 skills de `skills/oficina/` **por mandato del propietario**, no por
  diseño especulativo — la regla contra skills especulativas sigue viva para
  todo lo demás.
- F0.B gana un paso B12 (desplegar la oficina: `office/deploy.sh` +
  `office/hermes/instalacion.md`) y el plan de validación del doc 09 §8 gana
  los checks de la oficina (instalacion.md §5).
- La retro semanal audita además: diffs de skills de oficina contra el repo,
  muestreo de que ninguna acción externa esquivó `oficina politica check`, y
  la lista de publicaciones autónomas bajo marcas de oficina.
- El resumen diario incluye siempre: gates pendientes, publicaciones de
  marcas de oficina (veto retroactivo) y breakers activos.
- Riesgo aceptado: el CLI/tablero es gobernanza, no frontera de seguridad —
  un agente malicioso podría editar JSON a mano. Mitigación: la frontera real
  siguen siendo las credenciales (Tier-0 fuera de la VM, marcas protegidas
  sin credenciales en la VM) + auditoría de la retro. Igual que en doc 09 §4.
