---
name: jdg-resumen-diario
description: Generar el resumen ejecutivo diario (08:00) y el informe profundo semanal (lunes 07:30) para el propietario vía Telegram. Sin actividad, sin mensaje.
---

# Resumen diario y semanal (Jefe de Gabinete)

Nivel de modelo: 1.

## Diario (08:00 Europe/Madrid)

1. Si no hubo actividad desde el último resumen → **no enviar nada**. El silencio es señal de respeto, no de fallo.
2. Formato exacto de `playbooks/tablero.md`: avance (1-3 líneas), gates pendientes (n + ids), gasto (€ día/mes + eventos de ventana), anomalías o "ninguna".
3. Máximo 10 líneas. Sin narrativa de proceso: solo qué cambió y qué espera al propietario.
4. Regenerar `ESTADO.md` en el repo con la misma información ampliada (commit + push).

## Semanal profundo (lunes 07:30)

Por línea de dominio: estado del pipeline, decisiones R0/R1 tomadas (para veto retroactivo), memos pendientes de GO, gasto acumulado vs presupuesto, próximos hitos. Cierra con las ≤3 cosas que necesitan al propietario esta semana, en orden.
