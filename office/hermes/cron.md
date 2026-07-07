# Cron del daemon Hermes — la oficina en marcha

La proactividad de la oficina la dispara el **cron nativo de Hermes Agent**
(doc 09: primitiva verificada del sustrato; la sintaxis exacta de alta de jobs
es **[TBV]** en la instalación — `hermes cron …` o config YAML según versión).
No hay ningún scheduler propio: un solo job de despacho mueve todo el tablero,
y las cadencias por departamento se ajustan desde el panel (campo
`cadencia_min`), sin tocar el cron.

| Cuándo (Europe/Madrid) | Job (prompt al agente raíz) | Skill que ejecuta |
|---|---|---|
| **cada 15 min** | «Ejecuta un ciclo de despacho de la oficina.» | `orquestador-despacho` |
| Diario 08:00 | «Resumen diario si hubo actividad; abre con `oficina estado` e incluye gates pendientes y publicaciones de marcas de oficina de las últimas 24 h.» | `jdg-resumen-diario` |
| Diario 08:05 | «Snapshot de ledger del día anterior (proveedores, rate-limits, € — cruza con `oficina gasto mes`).» | `ledger` |
| Lunes 07:30 | «Informe profundo semanal por línea de dominio y por departamento de la oficina.» | `jdg-resumen-diario` + `ledger` |
| Domingo 18:00 | «Retro semanal: outcomes, auditoría de TODAS las skills auto-creadas y de los diffs de las skills de oficina; verifica por muestreo que ninguna acción externa esquivó `oficina politica check`.» | `retro-semanal` |
| Día 1, 09:00 | «Mantenimiento mensual: TTLs de knowledge/, tamaño de memoria, cierre de coste, archivar tareas `done` >30 días del tablero.» | `rol-documentalista` + `ledger` |

Notas:
- El job de despacho es idempotente y barato: si no hay intake, ni gates
  decididos, ni pulsos vencidos, ni WIP libre, termina en segundos (nivel de
  modelo 1-2). Los pulsos por departamento salen de `oficina pulso pendientes`
  (determinista), así que **no** se añade un cron por departamento.
- Además del cron, el gateway Telegram dispara `orquestador-despacho` en
  cuanto el propietario escribe (el intake no espera al siguiente tick).
- Los mensajes `APRUEBO/RECHAZO <id>` siguen el flujo del doc 06 §2: el
  orquestador los transcribe al tablero con la cita literal
  (`oficina gate decidir … --aprobacion "…"`). Desde el panel, la decisión
  queda registrada directamente.
