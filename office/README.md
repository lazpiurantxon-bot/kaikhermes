# office/ — la oficina autónoma (tablero + CLI + panel)

Implementación de `operating-model/10-oficina-autonoma.md` (ADR-004). **La
agencia vive en Hermes Agent** (skills en `skills/oficina/`, cron del daemon,
subagentes aislados); aquí está solo la parte que la gobernanza exige que sea
determinista, y la interfaz del propietario.

```
office/
├── core/            # tablero (archivos JSON) + política de marcas — stdlib puro
│   ├── store.py     #   estados, WIP, breakers, gates, ledger, eventos
│   └── policy.py    #   allow/gate/deny fail-closed (la regla de marcas)
├── bin/oficina      # CLI de los agentes (y del orquestador) — stdlib puro
├── panel/           # panel web del propietario (FastAPI + UI estática)
├── seeds/           # departamentos, marcas protegidas y control iniciales
├── hermes/          # cableado con el daemon: instalacion.md + cron.md
├── systemd/         # unidad del panel (usuario)
├── tests/           # pytest — política, tablero, CLI y API del panel
└── deploy.sh        # despliegue idempotente en la VM
```

## Despliegue en la VM (2 pasos)

```bash
# 1. Tablero + CLI + panel (idempotente)
cd ~/office/kaikhermes && bash office/deploy.sh

# 2. Conectar Hermes (skills, prompt del raíz, cron) — con el daemon ya vivo
#    → office/hermes/instalacion.md  (los [TBV] se verifican ahí)
```

Panel: `http://127.0.0.1:8787`, token en `~/.hermes-office/panel.yaml`.
Escucha **solo en localhost a propósito**; desde tu máquina:
`ssh -L 8787:127.0.0.1:8787 <vm>` → `http://localhost:8787`.

## Probar sin la VM (demo local)

```bash
cd office
export OFICINA_STATE=/tmp/oficina-demo PANEL_TOKEN=demo PANEL_CONFIG=/dev/null
python3 bin/oficina init && python3 -m panel.main   # → http://127.0.0.1:8787
# En otra terminal, simula el trabajo de los agentes:
OFICINA_STATE=/tmp/oficina-demo python3 bin/oficina intake add "analiza el mercado de geles" --por gabinete
OFICINA_STATE=/tmp/oficina-demo python3 bin/oficina tarea asignar T-0001 --dept mercado --por gabinete
OFICINA_STATE=/tmp/oficina-demo python3 bin/oficina tarea empezar T-0001 --por dep-mercado
```

## Tests

```bash
cd office && python3 -m pytest tests/ -q     # requiere: pip install pytest httpx fastapi uvicorn pyyaml
```

## Contratos clave

- **CLI (agentes):** `oficina estado | intake add | tarea … | politica check |
  gate … | marca … | gasto … | pulso … | evento …`. Exit codes de política:
  0 allow · 3 gate · 4 deny. Ver `skills/oficina/oficina-protocolo/SKILL.md`.
- **API (panel):** `GET /api/estado`, `POST /api/intake`, `POST /api/tareas`,
  `POST /api/tareas/{id}/accion`, `POST /api/gates/{id}/decidir`,
  `POST /api/departamentos/{slug}/accion`, `POST /api/control`,
  `POST /api/marcas`, `GET /api/eventos`, `GET /healthz`. Auth: Bearer token.
- **Seguridad:** el tablero es capa de gobernanza (previene accidentes y deja
  rastro), no frontera de seguridad; la frontera son las credenciales que la
  VM no tiene (doc 09 §4). El panel nunca se expone a Internet.
