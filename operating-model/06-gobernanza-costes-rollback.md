# 06 — Gobernanza, supervisión humana, costes y rollback

## 1. Niveles de riesgo (mapean tu B4 a mecanismo)

| Nivel | Definición | Ejemplos | Mecanismo |
|---|---|---|---|
| **R0** | Interno, reversible, sin gasto nuevo | Investigar, redactar borradores, código en branch, issues, docs | Autónomo. Queda en el log de acciones |
| **R1** | Interno pero persistente o con gasto dentro de límites | Deploy interno, crear repo, backup config, gasto ≤ límite de experimento | Autónomo + entrada destacada en resumen diario |
| **R2** | Público bajo tu marca, prod sin usuarios reales en dominio público, gasto que roza umbral | Publicar en `ezti.net`, post en redes, deploy público de demo | **Gate humano**: `APRUEBO <id>` por Telegram, o review de PR |
| **R3** | Terceros reales, usuarios/clientes, dinero recurrente, legal | Enviar email a un copacker, activar servicio con clientes, comprar dominio/suscripción, todo lo contractual | **Gate humano reforzado**: aprobación explícita + registro en PR/ADR; sin expiración implícita |
| **Prohibido** | — | Tier-0 (banca, empleador, Hacienda con presentación, identidad); presentación fiscal; firma de contratos; datos de huéspedes; publicar/negociar música (hasta resolver E13) | No existe ruta en el sistema. Pedirlo = error a reportar |

Reglas: en caso de duda entre dos niveles, se aplica el **superior**; la clasificación la hace el JdG en TRIAGE y el Contralor la audita; relajar cualquier límite exige tu autorización explícita + semanas sin errores (tu propia condición en B4), y se registra como ADR con fecha.

## 2. Flujo de aprobación (Telegram)

Cada solicitud de gate llega como mensaje autocontenido:

```
[GATE R2] #47 — Publicar landing EZTI v2 en ezti.net
Qué: reemplaza la landing actual por v2 (ES/EU/EN).
Por qué: checklist de claims OK, QA aprobado, staging: <url>
Rollback: revert al deploy anterior de CF Pages (1 clic, <1 min).
Responde: APRUEBO 47 / RECHAZO 47 <motivo> / PREGUNTA 47 <texto>
```

- El gateway (determinista) valida que la respuesta viene de tu chat ID y la registra en el ledger con timestamp. La aprobación es **por ítem**, nunca por lote implícito ("aprueba todo lo de hoy" no existe).
- Silencio = pendiente. Nada se ejecuta por timeout.
- Las aprobaciones R3 quedan además referenciadas en el PR o ADR correspondiente para auditoría a largo plazo.

## 3. Resúmenes ejecutivos (señal, no ruido)

- **Diario (si hubo actividad):** ≤10 líneas: qué avanzó, qué espera tu GATE, gasto del día, anomalías. Sin actividad → sin mensaje.
- **Profundo (2–3/semana o semanal según carga):** por línea de dominio: estado del pipeline, decisiones R0/R1 tomadas (para tu veto retroactivo), memos go/no-go pendientes, gasto acumulado vs presupuesto, próximos hitos.
- **Presentación de opciones:** cuando haya varias estrategias válidas, recibes un memo con ≤3 opciones, cada una con coste/riesgo/reversibilidad y **una recomendación argumentada**. Nunca una lista abierta de posibilidades sin postura — eso es devolverte el trabajo.

## 4. Costes: ledger de dos divisas y circuit breakers

El Contralor lleva dos contabilidades separadas porque tu situación tiene dos monedas:

1. **€ reales:** APIs de pago, infra fuera de créditos, SaaS, compras. Presupuesto: coste incremental objetivo <100–150 €/mes; techo 300 €/mes total; ≤20–30 € por experimento.
2. **Capacidad de suscripción:** eventos de rate-limit y ventanas premium consumidas (Claude Pro). No cuesta euros pero es el recurso escaso que limita la oficina; medirlo es lo que permitirá decidir con datos si conviene un plan superior (revisión en F2).

Circuit breakers automáticos (deterministas, no dependen de juicio de ningún LLM):
- Gasto real de experimento alcanza su límite → tareas del experimento se pausan + alerta.
- Gasto mensual proyectado >80% del techo → freno a todo gasto R1 nuevo hasta tu OK.
- ≥3 fallos consecutivos del mismo job programado → job deshabilitado + alerta (evita bucles que queman capacidad).
- Acción clasificada R2+ intentando ejecutarse sin registro de aprobación → bloqueo duro + incidencia.

**Kill switch global:** comando de Telegram (`PARA TODO`) que pausa scheduler y colas; solo se rearma manualmente. Se prueba en F0, no cuando haga falta.

## 5. Rollback (resumen operativo; detalle en doc 02 §7)

Toda aprobación R2+ lleva su plan de rollback **adjunto en la propia solicitud**. Si el rollback de algo no se puede describir en dos líneas, la acción no está lista para pedirte aprobación. Jerarquía: revert de git / redeploy de tag anterior / restore de backup / recreación de VM desde bootstrap. Los rollbacks ejecutados se registran como incidencia + entrada de retro: un rollback no es vergüenza, es el sistema funcionando; lo que sería inaceptable es necesitarlo y no tenerlo.

## 6. Auditoría

Cadena completa reconstruible para cualquier acción: **issue → spec → branch/PR → veredicto QA → aprobación (id, timestamp, canal) → deploy/tag → efecto observado**. El log de acciones (SQLite) y git se complementan: git para contenido, ledger para eventos. La retro semanal muestrea aleatoriamente 2–3 acciones y verifica que la cadena está íntegra — la auditoría también se audita.
