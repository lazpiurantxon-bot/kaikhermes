#!/usr/bin/env bash
# bootstrap.sh — VM nueva de Mandi desde cero. Idempotente. Ubuntu 24.04.
# NO ejecutar contra GCP hasta cumplir las 5 precondiciones de ADR-002
# (ver infra/runbook-vm.md). La VM debe poder recrearse en <30 min con este script.
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

echo "== [5/6] Cron de mandi (watchdog 5 min, ledger check diario) =="
crontab -u mandi - <<'CRON'
*/5 * * * * cd /srv/mandi/services && /usr/bin/python3 watchdog/watchdog.py >> /srv/mandi/state/watchdog.log 2>&1
15 8 * * *  cd /srv/mandi/services && /usr/bin/python3 ledger/ledger.py check >> /srv/mandi/state/ledger.log 2>&1
CRON

echo "== [6/6] Siguientes pasos manuales =="
cat <<'EOF'
1. Clonar el repo de gobierno como usuario mandi y copiar services/ a /srv/mandi/services/
2. Crear /srv/mandi/services/gateway-telegram/.env desde .env.example (chmod 600, chown mandi)
3. Ejecutar la prueba del kill switch: python3 services/tests/test_kill_switch.py
4. Arrancar: cd /srv/mandi/services && docker compose -f docker-compose.yml up -d
5. Verificar: enviar ESTADO al bot por Telegram
EOF
echo "bootstrap completado."
