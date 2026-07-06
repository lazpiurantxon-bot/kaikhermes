# [ARCHIVADO — ADR-003] Servicios deterministas pre-Hermes

> **Estos servicios NO se despliegan.** Sustituidos por las piezas nativas de Hermes Agent (gateway, cron, memoria) por decisión del propietario (ADR-003, 2026-07-06). Se conservan como referencia y rollback. El test del kill switch cumplió en su día la precondición 5 de ADR-002.

# Servicios deterministas (capa 24/7, SIN LLM)

Tres piezas, todas stdlib de Python 3 (cero dependencias externas — auditables línea a línea):

| Servicio | Qué hace | Cómo corre |
|---|---|---|
| `gateway-telegram/` | Intake (`IDEA:`), gates (`APRUEBO/RECHAZO/PREGUNTA <id>`), kill switch (`PARA TODO`/`REANUDA`), estado (`ESTADO`), envío del outbox | Docker, long-polling, `restart: unless-stopped` |
| `ledger/` | Dos divisas: € reales y eventos de suscripción (rate-limits). Circuit breakers. CLI | Invocado por sesiones/cron; `check` diario vía cron |
| `watchdog/` | Healthchecks HTTP, disco, backup del estado (local + GCS opcional), alertas vía outbox | Cron cada 5 min |

## Contrato de estado compartido

Un único SQLite: `/srv/mandi/state/mandi.db` (variable `MANDI_DB`). Tablas:

- `kv` — clave/valor. **`pausado='1'` es el kill switch**: todo job programado DEBE comprobarlo antes de arrancar y abortar si está activo. El watchdog sí corre en pausa (es monitorización, no trabajo).
- `intake` — ideas/mensajes entrantes pendientes de TRIAGE.
- `gates` — solicitudes de aprobación con estado (`pendiente/aprobado/rechazado`), timestamp y respuesta. **Silencio = pendiente; jamás se ejecuta por timeout.**
- `outbox` — mensajes que cualquier servicio/sesión encola para que el gateway los envíe al propietario.
- `spend` / `sub_events` / `acciones` — ledger y log de acciones.

## Seguridad

- El gateway solo acepta mensajes del `OWNER_CHAT_ID`; el resto se registra y se ignora.
- Cada servicio ve únicamente su `EnvironmentFile` (permisos 600). El token de Telegram solo lo tiene el gateway.
- Ningún servicio tiene credenciales de GitHub, Cloudflare ni Gmail.

## Prueba del kill switch (precondición de VM, ADR-002)

```
python3 services/tests/test_kill_switch.py
```
Verifica: `PARA TODO` marca `pausado=1`; un job que respeta el contrato aborta; `REANUDA` lo rearma. Se ejecuta en local/CI antes de tocar GCP.
