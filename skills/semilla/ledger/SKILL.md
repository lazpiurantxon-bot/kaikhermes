---
name: ledger
description: Contabilidad de dos divisas - euros reales y ventanas de suscripción consumidas. Registrar cada gasto, cada evento de rate-limit y cada escalado por falta de capacidad. Informe semanal y avisos de umbral.
---

# Ledger (Contralor de gasto)

Nivel de modelo: 1. Si Hermes expone métricas nativas de uso por proveedor (verificación V5), esta skill solo agrega e informa; si no, registra manualmente por tarea.

## Qué se registra (en `knowledge/core/ledger/AAAA-MM.md`, apéndice por evento)

- **€ reales:** cualquier gasto (API de pago, servicio, compra aprobada) con concepto y experimento asociado.
- **Ventanas:** eventos de rate-limit por proveedor (Claude Pro / ChatGPT-Codex / Vertex); tareas pausadas por falta de ventana; escalados al arquitecto por falta de nivel 3.
- **Gates económicos:** cada aprobación de gasto con su id.

## Umbrales (del acta, C6-C8) y acciones automáticas

| Condición | Acción |
|---|---|
| Experimento alcanza 20-30 € | Pausar sus tareas + avisar al propietario |
| Proyección mensual >80% del techo (300 €) | Freno a gasto R1 nuevo + aviso |
| ≥5 rate-limits en 24h en un proveedor | Anotar + degradar rutina a otro proveedor de la cadena §5 del PLAN |
| ≥3 escalados/semana por falta de nivel 3, 2 semanas seguidas | Activar la regla de revisión de plan (PLAN §5) — decide el propietario |

## Informe semanal (alimenta el resumen del lunes)

€ del mes vs techo · desglose por concepto · eventos de ventana por proveedor · tendencia. Sin narrativa: números y una línea de lectura.
