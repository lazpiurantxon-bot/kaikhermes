# Quickstart F0 — arranque de la VM de Hermes (procedimiento real)

Procedimiento efectivamente ejecutado en `hermes-core` (e2-small, Ubuntu 24.04, europe-southwest1-a). Es la fuente de verdad del bring-up F0. `infra/bootstrap.sh` es el objetivo de hardening más completo para F1 (usuario de servicio dedicado, firewall, unattended-upgrades); en F0 se corre Hermes como usuario de login sobre esta VM dedicada — el límite de aislamiento es la propia VM, que no contiene secretos Tier-0.

## Paso 1 — herramientas base
```bash
sudo apt-get update -y && sudo apt-get install -y curl git
```

## Paso 2 — instalar Hermes Agent (CLEAN-ROOM)
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```
- **PROHIBIDO** `hermes claw migrate` y cualquier importación desde OpenClaw (`openclaw-core`) o config previa. `~/.hermes` nace en blanco (ADR-003).
- Si el instalador ofrece migrar/importar → **NO**.
- Fallback si el instalador falla: `git clone --depth 1 --branch v2026.7.1 https://github.com/NousResearch/hermes-agent.git` y seguir su README.

## Paso 3 — comprobar
```bash
source ~/.bashrc 2>/dev/null
hermes doctor || hermes --help
```
Si `hermes` no se encuentra, revisar la salida del instalador (PATH) o abrir sesión SSH nueva.

## Paso 4 — auth de modelos (`hermes model`) — orden previsto
1. **OpenAI Codex** (device-code, usa ChatGPT Plus) → backend por defecto del daemon (rutina).
2. **Anthropic OAuth** → nivel 3. **[TBV crítico]** la doc cita "Claude Max + créditos"; aquí se verifica si el plan **Pro** basta. Si no: nivel 3 se escala a Claude Code (repo).
3. **Vertex AI** (service account, créditos GCP) → bulk barato.

## Paso 5 — gateway Telegram (@Tartaloagentbot)
Tras validar al menos un backend. Regenerar token en BotFather justo antes. DM pairing con la cuenta del propietario + probar rechazo de cuenta ajena.

## Paso 6 — plan de validación
Issue #5 / `operating-model/09-arquitectura-hermes.md` §8. Ningún gate de autonomía se relaja hasta completarlo.

## Notas del bring-up (2026-07-06)
- ufw/unattended-upgrades diferidos a F1 para evitar riesgo de lockout durante el primer arranque (el firewall de GCP ya controla el ingress). Se añaden como hardening en F1.
- Terminal backend: se arranca con el default; se conmuta a Docker en la validación (doc 09 §8, punto sandbox).
