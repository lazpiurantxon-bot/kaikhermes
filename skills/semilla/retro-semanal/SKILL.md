---
name: retro-semanal
description: Retrospectiva de los domingos 18:00 - outcomes de la semana, auditoría de TODAS las skills auto-creadas, propuestas de mejora como PR. Es el órgano de mejora continua gobernada.
---

# Retro semanal / Mejora continua

Nivel de modelo: 2. Programada: domingos 18:00 Europe/Madrid.

## Procedimiento

1. **Outcomes:** qué se cerró, qué se mató (y si se mató a tiempo), qué se atascó y por qué. Incidencias repetidas ≥2 veces = señal prioritaria.
2. **Auditoría de skills (el control clave del sustrato):** diff de `~/.hermes` skills contra la semana anterior. Para CADA skill auto-creada o auto-parcheada:
   - ¿Implica acción externa (publicar, contactar, gastar, desplegar)? → ¿lleva el gate R2/R3 dentro del procedimiento? Si no: **corregir o borrar esa misma semana.**
   - ¿Es útil y correcta? → proponer su canonización al repo vía PR (`skills/proposed/`).
   - ¿Contradice un playbook, el acta o una ADR? → borrar y registrar.
3. **Auditoría de trazabilidad:** muestrea 2-3 acciones de la semana y verifica la cadena issue→spec→PR→QA→gate→resultado. Huecos = incidencia.
4. **Ledger:** revisa el informe semanal; si hubo ≥3 escalados por falta de ventana nivel-3 esta semana Y la anterior, marca la regla de revisión de plan (PLAN §5) para el propietario.
5. **Propuestas:** mejoras de proceso/skills como PRs — **nunca automerge**; el propietario o QA humano decide según el nivel (doc 03 §4).
6. Patrón repetido ≥2 veces en trabajo real → borrador de skill en `skills/proposed/` con criterios de éxito y contraindicaciones.
7. Salida: informe de retro breve al propietario (parte del semanal del lunes) + PRs abiertos.
