# ADR-001 — Adopción del operating model y GO condicionado a F0

- **Fecha:** 2026-07-06
- **Estado:** aceptada
- **Nivel:** R1 (gobernanza interna)

## Contexto

El propietario revisó el diseño de FASE 2 (`operating-model/`) y dio **GO condicionado** para F0: la ejecución de infraestructura queda supeditada a un parche correctivo previo del operating model (ver ADR-002).

## Decisión

Se adopta el operating model descrito en `operating-model/` (docs 00–08) como marco vinculante del sistema, junto con el acta `fase-1-respuestas.md`. F0 arranca tras el commit correctivo.

## Consecuencias

- Toda acción del sistema se clasifica R0–R3 según doc 06.
- Los cambios al operating model se registran como ADR + commit, nunca como edición silenciosa.
- El criterio de éxito de F0 es el definido en doc 08 §1.
