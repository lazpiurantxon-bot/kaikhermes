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

## Decisiones pendientes

1. Qué es `kaikuv1` (inventario de metadatos) → determina repave vs VM nueva para Hermes.
2. Destino de `comfy-models` (mantener como activo audiovisual / borrar).
3. Snapshot + borrado diferido de `openclaw-core` (cuarentena del sistema anterior).
