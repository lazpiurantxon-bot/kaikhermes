# Convenciones del tablero (GitHub Issues)

El tablero vive en los Issues de `kaikhermes`. Un issue = una iniciativa o tarea con trazabilidad completa.

## Título

`[<FASE|dominio>] <qué>` — ejemplos: `[F0] Precondiciones VM`, `[EZTI] Sprint 1: shortlist copackers`.
Mientras no existan labels configurados, el estado y el riesgo van en el cuerpo del issue con este bloque al inicio:

```
Estado: INTAKE|TRIAGE|BRIEF|SPEC|PLAN|BUILD|QA|GATE|DEPLOY|OPERATE|RETRO|ARCHIVADO
Riesgo: R0|R1|R2|R3
Dominio: ezti|core|musica|hotel
Owner: <rol>
```

## Reglas

1. Toda transición de estado se anota como comentario con fecha y motivo (una línea basta).
2. Los artefactos (specs, informes, PRs, deploys) se enlazan desde el issue; lo no enlazado no existe.
3. Un issue R2+ no pasa de GATE sin cita del identificador de aprobación del gateway (`gate <id>: aprobado <timestamp>`).
4. Iniciativas muertas → comentario con motivo de kill + estado ARCHIVADO. Matar pronto es éxito.
5. WIP limit: máximo 2 iniciativas en BUILD/QA/DEPLOY simultáneamente.

## `ESTADO.md`

El JdG lo regenera al final de cada sesión: qué hay en cada estado, gates pendientes, gasto del período, verificaciones abiertas. Es la vista de 30 segundos del propietario.

## Resumen diario (formato, vía Telegram)

```
[MANDI diario — <fecha>]
Avance: <1–3 líneas>
Gates pendientes: <n> (ids)
Gasto: <€ hoy / € mes> · Sub: <eventos rate-limit>
Anomalías: <o "ninguna">
```
Sin actividad → sin mensaje.

## Formato de solicitud de gate

```
[GATE R2|R3] <id> — <título>
Qué: <1 línea>
Por qué ahora: <1 línea + enlaces (issue, staging, PR)>
Rollback: <≤2 líneas — si no cabe en 2 líneas, no está listo>
Responde: APRUEBO <id> / RECHAZO <id> <motivo> / PREGUNTA <id> <texto>
```
