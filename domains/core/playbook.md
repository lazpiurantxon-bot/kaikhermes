# Playbook de dominio — Core (Hermes/Mandi)

**Línea:** el propio sistema operativo agéntico. **Piloto técnico.**

## Prioridad de calidad (acta G20)

Calidad > velocidad > coste. Parchear mal la base sale más caro que construirla despacio.

## Límites duros

- Ningún cambio de comportamiento del sistema (playbooks, skills, límites de riesgo, autonomía) sin PR con merge humano. Sin excepciones.
- Los servicios 24/7 son deterministas: **prohibido** meter llamadas a LLM en gateway, ledger o watchdog.
- Secretos según doc 02: Tier-0 jamás; Tier-1 segmentado por servicio con mínimo privilegio.
- Precondiciones de VM (ADR-002) antes de cualquier acción contra GCP.
- Relajar cualquier límite: autorización explícita del propietario + semanas sin errores + ADR.

## Convenciones

- Branches: `mandi/<dominio>-<slug>`. Un worktree/branch por iniciativa.
- Todo servicio nuevo: Dockerfile + healthcheck + entrada en runbook + rollback descrito antes del primer deploy.
- Estado compartido de servicios: SQLite en `/srv/mandi/state/mandi.db` (contrato en `services/README.md`).

## KPIs de línea

Uptime de servicios internos; 0 acciones R2+ sin gate registrado; cadena de trazabilidad íntegra en el muestreo semanal; incidencias repetidas tendiendo a 0.
