# Inventario GCP (precondición 2, ADR-002) — v1

- **Fecha:** 2026-07-06 · **Fuente:** `gcloud compute instances/disks list` ejecutado por el propietario en Cloud Shell.
- **valido_hasta:** 2026-08-06 (revalidar antes de operaciones de infra).
- **Método:** solo metadatos, sin inspeccionar contenido de discos (clean-room).

## Proyecto y región

- Proyecto: `project-0b4f1868-2c05-493e-999`
- Región principal: `europe-southwest1` (Madrid) — bien para RGPD/latencia España.
- Config Cloud Shell activa: `cloudshell-20559`.
- **Aviso no bloqueante:** error "Regional Access Boundary / Account not found for email: ce71e9c893|lazplurantxon@gmail.com" (email mal escrito, no es el principal). Los listados funcionaron igual. Posible IAM/service-account obsoleto o access boundary regional. Vigilar si aparecen errores de permisos.

## Instancias

| Nombre | Tipo | Zona | Estado | IP ext. | Disco | Interpretación |
|---|---|---|---|---|---|---|
| `openclaw-core` | e2-standard-2 | europe-southwest1-a | TERMINATED | — | 50 GB | **Sistema anterior = OpenClaw.** Objetivo del clean-room. NO migrar (`hermes claw migrate` prohibido). Snapshot → cuarentena → borrado con aprobación. |
| `kaikuv1` | e2-standard-2 | europe-southwest1-a | RUNNING | 34.175.34.38 | 100 GB | **Desconocido.** Inventariar (metadatos) antes de decidir repave vs VM nueva. |

## Discos

| Nombre | Tamaño | Ubicación | Estado | Adjunto a | Nota |
|---|---|---|---|---|---|
| `comfy-models` | 250 GB pd-balanced | europe-west4-a | READY | — (suelto) | Probable ComfyUI (imagen/vídeo). ~28 €/mes sin uso. **Decisión del propietario:** ¿activo audiovisual/música o abandonado? |
| `kaikuv1` | 100 GB pd-balanced | europe-southwest1-a | READY | kaikuv1 | — |
| `openclaw-core` | 50 GB pd-balanced | europe-southwest1-a | READY | openclaw-core (term.) | Factura aunque la VM esté parada. |

## Coste ocioso identificado

- `comfy-models` (250 GB): ~28 €/mes sin adjuntar.
- `openclaw-core` (50 GB): ~6 €/mes con la VM parada.
- Total sangrado ~34 €/mes sobre un presupuesto de 100–300 €/mes → material.

## Decisiones tomadas (2026-07-06)

1. **VM de Hermes: NUEVA y dedicada** (`hermes-core`, e2-small, europe-southwest1-a). No se repavimenta ni se toca `kaikuv1`.
2. **`kaikuv1`: se deja intacto.** El `describe` no reveló workload (solo Ops Agent, osconfig, claves SSH; service account por defecto con scopes básicos; tag `acceso-ssh`; claves SSH expiradas el 2026-06-30). Sigue RUNNING (~49 €/mes). **Sin clasificar** — pendiente que el propietario aclare para qué es (posible ahorro futuro o servicio necesario). No bloquea nada.
3. **`comfy-models`: BORRAR** (autorizado; experimento). Ahorro ~28 €/mes.
4. **`openclaw-core`: dejar de momento** (sin snapshot ni borrado por ahora, por decisión del propietario). Sigue en TERMINATED; disco ~6 €/mes.

## VM nueva de Hermes — especificación

- Nombre: `hermes-core` · Tipo: **e2-small** (2 vCPU compartida, 2 GB) · Zona: europe-southwest1-a (Madrid).
- Disco: 30 GB pd-balanced, Ubuntu 24.04 LTS.
- Coste estimado: ~13–16 €/mes on-demand + ~1 €/mes disco → **cubierto por créditos GCP** (coste real ≈ 0).
- **Ruta de upgrade:** si el daemon + Docker + subagentes agotan la RAM, subir a e2-medium (4 GB, ~24 €/mes) es un `stop` + cambio de tipo + `start`, sin reinstalar.
