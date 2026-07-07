# Skills semilla — la oficina, implementada

13 skills (catálogo cerrado en `PLAN.md` §3), formato compatible agentskills.io: un directorio por skill con `SKILL.md` (frontmatter + procedimiento). Se instalan en Hermes en el paso F0.B-B7.

**Reglas:**
1. La versión de este repo es la **canónica**. Si Hermes parchea una skill semilla en uso, la retro semanal reconcilia: o el parche se trae aquí vía PR, o se revierte allí.
2. Toda skill con acción externa lleva su gate R2/R3 **dentro del procedimiento** — no es opcional ni configurable.
3. No se añaden skills a `semilla/` por diseño especulativo: las nuevas nacen del ciclo gobernado (`skills/proposed/` → prueba ×2 → QA → merge humano → `skills/approved/`).
4. Toda skill asume cargado el playbook del dominio activo (`domains/<dominio>/playbook.md`) y respeta el acta (`operating-model/fase-1-respuestas.md`).
