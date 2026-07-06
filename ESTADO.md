# ESTADO — 2026-07-06

**Fase:** F0 (Fundación) en curso · **Pausa:** no · **Gasto real del mes:** 0 €

## Hecho hoy

- Parche correctivo pre-F0 aplicado y registrado (ADR-002); ADR-001 adopta el operating model.
- Estructura del repo de gobierno: `domains/` (4 playbooks con límites legales embebidos), `playbooks/` (roles + tablero), `knowledge/`, `decisions/`, `skills/`, `infra/`, `services/`.
- Servicios deterministas escritos y verificados en CI local: gateway-telegram (intake, gates, kill switch), ledger (dos divisas, circuit breakers), watchdog (salud, disco, backups). **Test del kill switch: verde** (precondición 5 de ADR-002 cumplida en local).
- `infra/bootstrap.sh` + `docker-compose.yml` + `runbook-vm.md` con las 5 precondiciones.
- **EZTI Sprint 1 (parcial):** 12 copackers candidatos con fuente ([#1](https://github.com/lazpiurantxon-bot/kaikhermes/issues/1)); dossier de compliance alimentario v1; borradores de contacto ES/EN en espera de gate.

## Esperando al propietario

| Qué | Issue | Por qué solo él |
|---|---|---|
| Precondiciones de VM (snapshot probado, inventario, coste) | [#2](https://github.com/lazpiurantxon-bot/kaikhermes/issues/2) | Credenciales GCP (Tier-1 aún no expuestas) |
| Bot de Telegram nuevo + chat ID | [#3](https://github.com/lazpiurantxon-bot/kaikhermes/issues/3) | Creación del secreto Tier-1 |
| Verificaciones V1–V3 (ultracode, Fable 5, Vertex, Routines) | [#4](https://github.com/lazpiurantxon-bot/kaikhermes/issues/4) | Datos de su cuenta/plan |

## Gates pendientes

Ninguno formalizado todavía (los envíos a copackers se solicitarán como gates R3 individuales cuando el gateway esté desplegado; hasta entonces, por este canal).

## Próximo (sin dependencias del propietario)

Sprint 1 segunda pasada: barrido de envasadores de miel con línea monodosis + verificación de fichas + priorización de 5–6 candidatos.
