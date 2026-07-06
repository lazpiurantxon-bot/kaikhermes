#!/usr/bin/env bash
# bootstrap.sh — hardening objetivo F1 (usuario de servicio dedicado, firewall,
# unattended-upgrades). Para el arranque F0 real ver infra/quickstart-f0.md
# (Hermes como usuario de login, ufw diferido). Idempotente. Ubuntu 24.04.
# La VM debe poder recrearse en <30 min con este script + el quickstart.
set -euo pipefail

echo "== [1/6] Paquetes base =="
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
  docker.io docker-compose-v2 ufw unattended-upgrades sqlite3 python3 git curl

echo "== [2/6] Firewall: denegar entrada salvo SSH =="
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw --force enable

echo "== [3/6] Actualizaciones de seguridad automáticas =="
dpkg-reconfigure -f noninteractive unattended-upgrades

echo "== [4/6] Usuario y directorios =="
id -u mandi &>/dev/null || useradd -m -s /bin/bash mandi
usermod -aG docker mandi
install -d -o mandi -g mandi -m 750 \
  /srv/mandi /srv/mandi/state /srv/mandi/state/backups \
  /srv/mandi/services /srv/mandi/deploys

echo "== [5/6] Workspace de la oficina =="
install -d -o mandi -g mandi -m 750 /srv/mandi/office

echo "== [6/6] Siguientes pasos manuales (ADR-003: sustrato Hermes Agent) =="
cat <<'EOF'
Como usuario mandi:
1. Instalar Hermes Agent limpio (release estable actual):
     curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
   PROHIBIDO: copiar config/memoria/skills del Hermes antiguo o usar 'hermes claw migrate' (clean-room, ADR-003).
2. hermes setup  → asistente completo
3. hermes model  → backends por orden: OpenAI Codex OAuth (rutina),
   Anthropic OAuth (nivel 3; verificar si el plan Pro basta), Vertex AI
   con service account (bulk, créditos GCP)
4. Gateway Telegram con el bot @Tartaloagentbot (token REGENERADO en
   BotFather justo antes): hermes gateway  → pairing DM con el propietario
   + probar rechazo de cuenta ajena
5. Clonar el repo de gobierno en /srv/mandi/office/ y cargar skills
   semilla y playbooks (operating-model/09 §9)
6. Completar el plan de validación (operating-model/09 §8) y registrar
   resultados en el issue #5
EOF
echo "bootstrap completado."
