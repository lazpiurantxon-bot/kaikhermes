# 02 — Clean-room, aislamiento, workspaces y secretos

## 1. Estado clean-room verificado

Hecho verificable, no promesa: el primer commit de esta fase en `kaikhermes` fue un **root commit** (branch `claude/multiagent-operating-model-fli2vq`), lo que demuestra que el repo estaba vacío. No se ha leído, listado ni importado ningún artefacto del sistema anterior.

**Regla permanente de importación:** ningún archivo, prompt, memoria, skill, credencial o configuración del sistema anterior entra en el nuevo sin autorización escrita tuya **ítem a ítem** (un mensaje que diga exactamente qué artefacto y para qué). El artefacto importado se revisa antes de integrarse y queda registrado en `decisions/` con fecha y motivo. Por defecto: nada.

## 2. Recomendación de repositorio (H24 — decidido con datos, no por inercia)

**Recomendación: `kaikhermes` se queda como repo de gobierno; cada producto tiene repo propio.**

- A favor de quedarse: está verificado vacío (clean-room de facto), ya es el branch designado y mover el gobierno a otro repo solo añadiría una migración sin eliminar ningún riesgo real de contaminación (no hay nada que contaminar).
- Separación por producto (`ezti-web`, prototipos, servicios): limita el blast radius, permite tokens de acceso **por repo** (fine-grained PAT), y evita que el repo de gobierno acumule código de producto.
- Único matiz: el nombre `kaikhermes` referencia el sistema anterior. Si eso te incomoda, renombrar el repo en GitHub es barato y no rompe nada (GitHub redirige). Decisión cosmética, tuya.

## 3. Infraestructura: repave, no reutilización

La VM existente tiene instalaciones previas de Hermes declaradas como no fiables. Reutilizarla violaría el clean-room y heredaría configuración desconocida.

1. **VM nueva** en GCP (e2-small basta para F0–F1; con créditos, coste real ≈ 0). Se crea desde `infra/bootstrap.sh` **versionado en este repo**: usuario no-root, Docker, systemd units del gateway/ledger/watchdog, ufw con denegación por defecto, actualizaciones automáticas de seguridad. La VM debe poder recrearse desde cero en <30 min — esa es la definición de "infraestructura limpia".
2. **VM antigua: cuarentena.** Snapshot de disco → parar todos los servicios/autostart → mantener 30 días apagada como archivo de solo lectura → borrar tras tu aprobación explícita. **Nunca** se montan sus volúmenes en la VM nueva. Si algún dato antiguo resulta necesario, se aplica la regla de importación ítem a ítem.
3. **Sin nostalgia de n8n:** los flujos previos no se migran. Lo que hacían se reimplementa (si merece la pena) como cron + código determinista o como Routine de Claude Code.

## 4. Workspaces y perfiles

```
VM:  /srv/mandi/
     ├── state/        # SQLite (ledger, logs de acciones), colas
     ├── services/     # gateway-telegram, watchdog (Docker/systemd)
     └── deploys/      # servicios internos desplegados

Sesiones de agentes (Claude Code):
     kaikhermes/                     # repo de gobierno (este)
     ├── operating-model/            # este diseño
     ├── domains/<dominio>/          # playbook + estado por línea
     ├── knowledge/  decisions/      # KB y ADRs (doc 03)
     ├── skills/  playbooks/         # capacidades gobernadas (doc 03)
     └── infra/                      # bootstrap.sh, runbooks

     <repo-producto>/                # un repo por producto
     └── worktrees/branches: mandi/<dominio>-<slug> por iniciativa
```

- **Perfiles en blanco:** cada repo lleva su `CLAUDE.md` escrito desde cero en esta fase. Prohibido importar CLAUDE.md, memorias o configuración del sistema anterior (regla de importación §1).
- **Un worktree/branch por iniciativa** (`mandi/ezti-copacker-shortlist`, `mandi/core-gateway`…): aísla trabajo en paralelo, hace el rollback trivial (borrar branch) y deja el diff como unidad de revisión.
- Los especialistas efímeros solo reciben los directorios que su encargo declara. El playbook de dominio del hotel, por ejemplo, prohíbe explícitamente pedir o aceptar datos de huéspedes aunque tú los pegues por error (respuesta estándar: "esto no puede entrar en el sistema").

## 5. Sandbox y contenedores

- Servicios en la VM: **Docker, uno por servicio**, sin privilegios, con volúmenes mínimos declarados (el gateway solo ve su cola y su token; el watchdog solo ve métricas y el bucket de backup). `docker-compose.yml` versionado.
- Trabajo agéntico: las sesiones de Claude Code ya corren en contenedores efímeros gestionados (verificado: este entorno). No se añade una capa extra de sandbox propia en F0 — sería complejidad sin amenaza que la justifique, dado que los secretos Tier-0 ni siquiera existen dentro del sistema.
- Código no confiable (dependencias nuevas, scripts de terceros): se ejecuta primero en contenedor descartable en la VM, nunca directamente sobre `state/`.

## 6. Secretos: dos niveles

**Tier-0 — nunca entran al sistema** (ni en env, ni en archivos, ni "solo esta vez"): banca; credenciales y sistemas del empleador (hotel); Hacienda o cualquier credencial con capacidad de presentación/firma; identidad digital crítica (certificado digital, Cl@ve); cuentas personales sensibles. Si un flujo "necesita" un Tier-0, el flujo está mal diseñado: se rediseña para que **tú** ejecutes ese paso.

**Tier-1 — segmentados, mínimo privilegio, revocables:**

| Secreto | Alcance | Quién lo ve |
|---|---|---|
| GitHub fine-grained PAT | Por repo, permisos mínimos (p. ej. solo `ezti-web`) | Sesión/servicio que trabaja ese repo |
| Telegram bot token | Solo el bot | Solo `gateway-telegram` |
| Cloudflare API token | Scoped a zona `ezti.net`, solo Pages/DNS necesarios | Solo el paso de deploy |
| GCP service account | Rol mínimo (escribir en bucket de backups; nada más) | Solo watchdog |
| Gmail OAuth (F1) | Scopes `gmail.readonly` + `gmail.compose` — **técnicamente incapaz de enviar** | Solo el flujo de borradores |

Almacenamiento: en la VM, archivos de entorno por servicio con permisos 600 propiedad del servicio (systemd `EnvironmentFile`), o GCP Secret Manager si crece el número. Rotación al menor indicio de fuga; todos los tokens deben poder revocarse individualmente sin tumbar el resto.

## 7. Checkpoints y rollback

| Capa | Mecanismo | Rollback |
|---|---|---|
| Código y docs | Git, PRs, tags de release | `git revert` / redeploy del tag anterior |
| Estado VM (`state/`) | Backup diario cifrado a bucket GCS + snapshot semanal de disco | Restaurar archivo/snapshot |
| Infra | `bootstrap.sh` idempotente versionado | Recrear VM desde cero (<30 min) |
| Despliegues internos | Imágenes Docker etiquetadas por versión | `docker compose` al tag anterior |
| Web pública (CF Pages) | Deploys inmutables de Cloudflare Pages | Revertir al deploy anterior en un clic |
| Decisiones | ADRs append-only en `decisions/` | Las decisiones no se borran: se supersede con nueva ADR |

Antes de cualquier acción R2+ o cambio de infra: checkpoint explícito (tag o snapshot) referenciado en la solicitud de aprobación, de modo que cada aprobación tuya lleve adjunto su camino de vuelta.
