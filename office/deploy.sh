#!/usr/bin/env bash
# Despliegue de la oficina en la VM (idempotente). Ejecutar como el usuario
# que corre el daemon Hermes:   bash office/deploy.sh
# Deja: tablero sembrado, CLI `oficina` en PATH, panel como servicio systemd
# de usuario en 127.0.0.1:8787. La parte Hermes (skills, cron, prompt raíz)
# está en office/hermes/instalacion.md — requiere el daemon ya instalado.
set -euo pipefail

OFFICE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${HOME}"
CFG_DIR="${HOME_DIR}/.hermes-office"
STATE_DIR="${OFICINA_STATE:-${HOME_DIR}/office/state}"
VENV="${CFG_DIR}/venv"
BIN_DIR="${HOME_DIR}/.local/bin"

echo "== Hermes Office deploy =="
echo "   repo:   ${OFFICE_DIR}"
echo "   estado: ${STATE_DIR}"

# 1. Tablero sembrado (idempotente: no pisa un estado existente)
mkdir -p "${STATE_DIR}"
OFICINA_STATE="${STATE_DIR}" python3 "${OFFICE_DIR}/bin/oficina" --por "owner:deploy" init >/dev/null
echo "✓ tablero sembrado"

# 2. CLI oficina en PATH
mkdir -p "${BIN_DIR}"
ln -sfn "${OFFICE_DIR}/bin/oficina" "${BIN_DIR}/oficina"
echo "✓ CLI: ${BIN_DIR}/oficina (asegúrate de que ~/.local/bin está en el PATH del daemon)"

# 3. Config del panel (token persistente; no se regenera si existe)
mkdir -p "${CFG_DIR}"
PANEL_CFG="${CFG_DIR}/panel.yaml"
if [[ ! -f "${PANEL_CFG}" ]]; then
  TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
  cat > "${PANEL_CFG}" <<EOF
# Panel de la oficina Hermes — config del propietario (NO subir a git)
host: 127.0.0.1
port: 8787
token: "${TOKEN}"
state_dir: "${STATE_DIR}"
EOF
  chmod 600 "${PANEL_CFG}"
  echo "✓ config creada: ${PANEL_CFG}"
else
  echo "✓ config existente respetada: ${PANEL_CFG}"
fi

# 4. Venv del panel
if [[ ! -x "${VENV}/bin/python" ]]; then
  python3 -m venv "${VENV}"
fi
"${VENV}/bin/pip" install --quiet --upgrade pip
"${VENV}/bin/pip" install --quiet -r "${OFFICE_DIR}/requirements-panel.txt"
echo "✓ venv del panel listo"

# 5. Servicio systemd de usuario (con fallback si no hay sesión de usuario)
UNIT_DIR="${HOME_DIR}/.config/systemd/user"
mkdir -p "${UNIT_DIR}"
sed "s|__OFFICE_DIR__|${OFFICE_DIR}|g" \
  "${OFFICE_DIR}/systemd/hermes-office-panel.service" > "${UNIT_DIR}/hermes-office-panel.service"
if systemctl --user daemon-reload 2>/dev/null; then
  systemctl --user enable --now hermes-office-panel.service
  loginctl enable-linger "$(whoami)" 2>/dev/null || true
  echo "✓ servicio: systemctl --user status hermes-office-panel"
else
  echo "⚠ systemd de usuario no disponible en esta sesión."
  echo "  Opción A (recomendada): reconecta por SSH normal y relanza deploy.sh"
  echo "  Opción B (manual):      PANEL_CONFIG=${PANEL_CFG} ${VENV}/bin/python -m panel.main"
  echo "                          (desde ${OFFICE_DIR}, p. ej. bajo tmux)"
fi

echo
echo "== Listo =="
echo "Panel:  http://127.0.0.1:8787  (solo local a propósito)"
echo "Túnel:  ssh -L 8787:127.0.0.1:8787 <esta-vm>   → http://localhost:8787"
echo "Token:  grep token ${PANEL_CFG}"
echo
echo "Siguiente: conectar Hermes → office/hermes/instalacion.md"
echo "(skills de la oficina, prompt del agente raíz y cron de despacho)"
