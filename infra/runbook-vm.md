# Runbook — VMs (creación de la nueva, cuarentena de la antigua)

## 0. Precondiciones obligatorias (ADR-002) — checklist

Sin las cinco marcas **no se ejecuta nada contra GCP**:

- [ ] **Snapshot probado** de la VM antigua: crear snapshot del disco → crear instancia temporal desde el snapshot → verificar que arranca y el disco monta → borrar la instancia temporal (el snapshot se queda). "Snapshot hecho" sin restauración probada NO cumple.
- [ ] **Inventario mínimo** de la VM antigua: `systemctl list-units --type=service --state=running`, `crontab -l` (por usuario), `docker ps`. Solo metadatos (nombres, puertos); **no inspeccionar contenido** de archivos ni datos (clean-room).
- [ ] **Coste mensual estimado** de la VM nueva, calculado con la calculadora de precios de GCP para la región elegida (orden de magnitud esperado para e2-small: decenas de €/mes; confirmar cifra real y delta contra créditos antes de crear).
- [ ] **Rollback documentado**: sección 3 de este runbook revisada y entendida.
- [ ] **Kill switch probado**: `python3 services/tests/test_kill_switch.py` en verde (local/CI).

Ejecutor: el propietario, o el sistema con las credenciales GCP que el propietario decida exponer (mínimo privilegio: rol de administración de instancias sobre el proyecto concreto, nada más).

## 1. Cuarentena de la VM antigua

1. Snapshot probado (precondición 1).
2. Parar servicios: `sudo systemctl stop <cada servicio del inventario>` + deshabilitar autostart.
3. Parar la instancia (`gcloud compute instances stop <vm-antigua>`); mantener 30 días.
4. Borrado definitivo: **solo con aprobación explícita del propietario** (pregunta abierta nº 9 del doc 08); el snapshot se conserva.
5. Nada de la VM antigua se monta ni copia a la nueva sin autorización ítem a ítem.

## 2. Creación de la VM nueva

```bash
gcloud compute instances create mandi-core \
  --machine-type=e2-small --zone=<zona-elegida> \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --boot-disk-size=30GB
# dentro de la VM:
sudo bash infra/bootstrap.sh   # idempotente; <30 min hasta operativo
```

Después: pasos manuales que imprime el propio bootstrap — instalación limpia de **Hermes Agent** (ADR-003), `hermes setup`, backends por suscripción, gateway Telegram con pairing, carga de skills semilla y **plan de validación** de `operating-model/09-arquitectura-hermes.md` §8.

## 3. Rollback

| Situación | Acción |
|---|---|
| La VM nueva sale mal | Borrarla y recrearla desde `bootstrap.sh` (nada valioso vive solo en la VM: estado con backup diario, código en git) |
| Pérdida de `state/` | Restaurar el último `mandi-YYYYMMDD.db` desde `state/backups/` o del bucket GCS |
| Hay que volver atrás del todo | La VM antigua sigue en cuarentena 30 días: arrancarla restaura el mundo anterior |
| Servicio roto tras cambio | `docker compose` al tag/commit anterior del repo |

## 4. Verificación post-instalación

La define el plan de validación de `operating-model/09-arquitectura-hermes.md` §8 (auth por suscripción, pairing DM + rechazo de terceros, command approval, kill switch del daemon, gobernanza de skills, cron, aislamiento de subagentes, visibilidad de gasto, sandbox Docker). Cada punto se registra con fecha en el issue #5. `hermes doctor` como diagnóstico general. **Añadido ADR-004:** los checks de la oficina de `office/hermes/instalacion.md` §5 (CLI en PATH de subagentes, despacho por cron, pulsos proactivos, exit codes de política, gates desde el panel, kill switch del tablero, panel no expuesto).

## 5. Servicio del panel de la oficina (ADR-004)

| Operación | Comando (usuario del daemon) |
|---|---|
| Desplegar/actualizar | `cd ~/office/kaikhermes && bash office/deploy.sh` (idempotente) |
| Estado / logs | `systemctl --user status hermes-office-panel` · `journalctl --user -u hermes-office-panel -f` |
| Parar / arrancar | `systemctl --user stop hermes-office-panel` / `…start…` (parar el panel NO para la oficina: la agencia vive en el daemon Hermes) |
| Acceso | solo localhost; desde tu máquina `ssh -L 8787:127.0.0.1:8787 <vm>` → `http://localhost:8787`; token en `~/.hermes-office/panel.yaml` |
| Backup del tablero | `~/office/state/` entra en el backup normal de la VM (`tar` basta; es estado operativo, lo institucional está en git) |
| Rollback | `systemctl --user disable --now hermes-office-panel`; el tablero puede borrarse y resembrarse con `oficina init` |
