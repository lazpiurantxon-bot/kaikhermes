# PLAN — Plano maestro del sistema (v1, 2026-07-06)

**Qué es esto:** la dirección completa y cerrada del sistema, desde el estado actual hasta la oficina en régimen. Todas las decisiones están tomadas aquí (o delegadas a árboles de decisión pre-resueltos en §5). No hay que decidir "el siguiente paso" nunca: se ejecuta este plan en orden, y solo se vuelve a decidir si un criterio de salida falla.

**Jerarquía documental:** este plan manda sobre el orden de ejecución; `operating-model/09` manda sobre la arquitectura; `operating-model/00-08` sobre gobernanza y dominios; el acta `fase-1-respuestas.md` sobre restricciones. Conflicto → gana el de más arriba en esta lista… salvo el acta, que gana siempre.

**Cómo retomar en cualquier sesión futura (humano o agente):** leer `PLAN.md` → `ESTADO.md` → issue del paso activo. Nada más.

---

## 1. El sistema completo, en una vista

```
┌─ TÚ (propietario) ────────────────────────────────────────────────┐
│  Telegram @Tartaloagentbot: gates, intake, resúmenes (≤5 min/día) │
│  GitHub: PRs y memos go/no-go (15-30 min, 2-3×/semana)            │
└─────────────┬─────────────────────────────────────────────────────┘
┌─────────────▼─────────────────────────────────────────────────────┐
│  HERMES AGENT — daemon en hermes-core (34.175.116.122, Madrid)    │
│  = LA OFICINA 24/7                                                │
│  · JdG (agente raíz): triaje, tablero, gates, resúmenes           │
│  · Subagentes aislados: Investigación/Estratega/Constructor/QA/   │
│    SRE/Documentalista (skills semilla §3)                         │
│  · Memoria episódica: ~/.hermes (SQLite+FTS5)                     │
│  · Cron §4: resumen diario, retro semanal, mantenimiento mensual  │
│  · Backends §5: Codex(rutina) Anthropic(crítico) Vertex(bulk)     │
│  · Ejecución en Docker (sandbox)                                  │
└─────────────┬─────────────────────────────────────────────────────┘
┌─────────────▼─────────────────────────────────────────────────────┐
│  REPO kaikhermes = LA VERDAD INSTITUCIONAL                        │
│  PLAN · ESTADO · operating-model/ · decisions/ · knowledge/ ·     │
│  domains/ · playbooks/ · skills/ · infra/ · Issues (tablero)      │
│  + repos de producto (ezti-web, prototipos…) según nazcan         │
└─────────────▲─────────────────────────────────────────────────────┘
              │ PRs, revisiones de arquitectura y QA crítico
   CLAUDE CODE (sobre tu Claude Pro) = ARQUITECTO EXTERNO
```

Líneas de dominio (estado objetivo): **core** (el sistema), **ezti** (piloto de negocio), **musica** (privado hasta E13), **hotel** (límites E12), y plantilla para futuras (hogar, deportes). Una línea nueva = carpeta en `domains/` + playbook + label — sin tocar arquitectura.

## 2. Estructura de archivos final (VM y repo)

```
VM hermes-core:
  ~/.hermes/               # config.yaml, credenciales OAuth, memoria, skills instaladas
  ~/office/
    ├── kaikhermes/        # este repo, clonado (working copy del daemon)
    └── repos/             # repos de producto que el daemon clone
  (F1: migración a usuario de servicio 'mandi' + ufw + unattended-upgrades
   según infra/bootstrap.sh; en F0 corre como usuario de login)

Repo kaikhermes (ya existe; se añade lo marcado *):
  PLAN.md  ESTADO.md
  operating-model/00-09
  decisions/ADR-001..003 (+ los que vengan)
  domains/{ezti,core,musica,hotel}/playbook.md (+specs/ +outreach/)
  knowledge/{INDEX.md, ezti/*, core/*}
  playbooks/{roles.md, tablero.md}
  skills/semilla/*          * catálogo §3, formato agentskills.io
  infra/{quickstart-f0.md, bootstrap.sh, runbook-vm.md}
  archive/pre-hermes-services/
```

## 3. Catálogo cerrado de skills semilla (la oficina, implementada)

Las escribo yo (Claude Code) en `skills/semilla/` — es trabajo mío, no tuyo. Se instalan en Hermes en el paso B7. Formato agentskills.io. **13 skills, ni una más en F0-F1** (todo lo demás debe nacer del ciclo gobernado de skills, no de diseño especulativo):

| # | Skill | Propósito | Gate embebido | Nivel modelo |
|---|---|---|---|---|
| 1 | `jdg-triaje` | Clasificar intake: dominio, riesgo R0-R3, prioridad, duplicados; crear/actualizar issue | — | 1-2 |
| 2 | `jdg-resumen-diario` | Formato del doc `playbooks/tablero.md`; sin actividad → sin mensaje | — | 1 |
| 3 | `jdg-gate` | Formular solicitud R2/R3 (qué/por qué/rollback ≤2 líneas), enviarla, **esperar**; silencio=pendiente | Es el gate | 2 |
| 4 | `rol-investigacion` | Investigar con fuente primaria+fecha+confianza; huecos declarados; propuesta a knowledge/ vía PR | — | 2 |
| 5 | `rol-estratega` | Brief→spec con criterios de aceptación congelados + memo ≤3 opciones con recomendación | Memo→GO humano si R2+/€ | 3 |
| 6 | `rol-constructor` | Implementar spec en branch `mandi/<dominio>-<slug>` con tests; no cambia criterios | — | 2 |
| 7 | `rol-qa` | Subagente separado; ejecutar criterios uno a uno; para no-código: verificación de fuentes/claims | Bloquea merge | 3 crítico / 2 rutina |
| 8 | `rol-sre` | Deploy según tabla doc 05 §4; rollback escrito antes del primer deploy de cada tipo | Prod → R2/R3 | 2 |
| 9 | `rol-documentalista` | Destilar a knowledge/ (fuente/fecha/TTL) y ADRs; INDEX ≤2 saltos | — | 1-2 |
| 10 | `retro-semanal` | Outcomes de la semana; **auditar TODAS las skills auto-creadas** (diff semanal): promover/corregir/borrar; proponer mejoras como PR | Merge humano | 2 |
| 11 | `ledger` | Registrar uso por proveedor, eventos rate-limit, € reales; informe semanal; avisos 80% presupuesto | — | 1 (o nativo si V5 lo da) |
| 12 | `ezti-claims` | Checklist 1924/2006 obligatorio sobre cualquier texto público de EZTI | Bloquea publicación | 3 |
| 13 | `outreach-r3` | Proceso de contacto con terceros: borrador → gate R3 individual → **el envío lo hace el propietario** | Es el gate | 2 |

Regla: skill auto-creada por Hermes con acción externa y sin gate embebido = defecto que la retro corrige o borra esa misma semana.

## 4. Cron (horarios cerrados, Europe/Madrid)

| Cuándo | Job | Skill |
|---|---|---|
| Diario 08:00 | Resumen diario (si hubo actividad) + cola de gates pendientes | 2 |
| Diario 08:05 | Ledger: snapshot de uso del día anterior | 11 |
| Lunes 07:30 | Informe profundo semanal (por línea de dominio) | 2+11 |
| Domingo 18:00 | Retro semanal + auditoría de skills | 10 |
| Día 1 de mes 09:00 | Mantenimiento: TTLs caducados en knowledge/, tamaño de memoria, coste mensual cerrado | 9+11 |

## 5. Backends y árboles de decisión PRE-RESUELTOS

Configuración objetivo: **Codex OAuth** (default, rutina) · **Anthropic OAuth** (nivel 3) · **Vertex AI** service account (bulk) · OpenRouter (emergencia, solo tras tu OK de fondearlo con ≤10 € prepago).

Cada incógnita pendiente tiene su rama ya decidida — al verificar, se ejecuta la rama, no se reabre el debate:

| Incógnita | Si SÍ | Si NO |
|---|---|---|
| V4: ¿Anthropic OAuth acepta tu plan **Pro**? | Daemon usa Claude para nivel 3 | Nivel 3 del daemon → se escala como issue al arquitecto (yo, vía repo); reevaluar Max **solo** si el ledger registra ≥3 escalados/semana durante 2 semanas seguidas |
| V2: ¿créditos GCP cubren Vertex? | Bulk a Vertex | Bulk se queda en Codex; no se contrata nada nuevo |
| ¿Command approval granular por comando/categoría? | Mapear R2/R3 a approval nativo + denylist | Gates solo vía skill 3 (`jdg-gate`) + denylist mínima; **compensación**: subagentes restringidos a trabajo R0 hasta F2 |
| ¿Se puede gatear la auto-creación de skills? | Activar gate para skills con acción externa | Cuarentena semanal de la retro (skill 10) es el único control — ya diseñado |
| V5: ¿métricas de uso nativas? | Usarlas; skill 11 solo agrega | Skill 11 registra manualmente por tarea |
| ¿Aislamiento real de subagentes? | Subagentes con todos los roles | Subagentes solo R0; QA y trabajo sensible en el daemon raíz secuencial |
| ¿`hermes` install falla / proyecto roto? | — | Plan B: clonar release fijada del repo oficial; Plan C (último recurso): reactivar `archive/pre-hermes-services/` como puente y reevaluar sustrato con ADR |

## 6. Secuencia completa de implementación

Cada fase tiene criterio de salida verificable. No se pasa a la siguiente sin cumplirlo. Si un paso falla → se aplica su rama de §5 o su rollback, no se improvisa.

### F0.B — Núcleo Hermes vivo (1-2 sesiones tuyas de ~30-60 min en la VM)
> Los comandos exactos ya están en `infra/quickstart-f0.md`. Yo te acompaño en sesión si quieres, pero el plan no requiere decisión alguna.

- B1. Base + instalar Hermes limpio (sin `claw migrate`) · B2. `hermes doctor` OK
- B3. `hermes model`: **Codex OAuth** → tarea de prueba por CLI
- B4. **Anthropic OAuth** → resuelve V4 (rama de §5)
- B5. **Vertex** service account → resuelve V2
- B6. Gateway: token de @Tartaloagentbot **regenerado**, pairing DM, prueba de rechazo con cuenta ajena
- B7. Clonar repo en `~/office/`, instalar skills semilla §3, cargar playbooks
- B8. Cron §4 configurado · B9. Backend Docker + prueba de sandbox (comando destructivo confinado)
- B10. Kill switch probado (Telegram y systemd) · B11. Checklist de validación (issue #5) completado y fechado

**Criterio de salida F0.B:** el daemon ejecuta de punta a punta una tarea real con gate — te propone algo por Telegram, apruebas con `APRUEBO`, lo hace, queda trazado en el issue. **Rollback global:** la VM es desechable; recrear cuesta <30 min.

### F0.C — La oficina toma el trabajo (sin ti, salvo gates)
- C1. El JdG-Hermes adopta el tablero (issues #1-#5) y `ESTADO.md`
- C2. Retoma Sprint 1 EZTI: verificación de fichas/emails de los 6 priorizados + borradores personalizados → tu cola de gates R3
- C3. Primer resumen diario real + primera retro

**Criterio de salida F0.C (= éxito de A3 del acta):** tienes en Telegram los 6 borradores listos para enviar, y el sistema funcionó sin que lo empujaras.

### F1 — Oficina operativa (semanas 2-5)
- Hardening VM (`bootstrap.sh` completo: usuario mandi, ufw, unattended-upgrades) — un fin de semana, sin prisa
- Gmail `readonly` + Calendar (doc 04 §2) — cuando aporten, no antes
- **EZTI:** respuestas de copackers → scoring → memo ≤3 finalistas (APP 1 completa) · web nueva en staging + kit de patrocinio (APP 3 hasta gate)
- Ciclo de skills gobernado rodando (≥2 retros) · ledger con primer informe mensual

**Criterio de salida F1:** pipeline INTAKE→RETRO demostrado en ≥2 iniciativas; ≥1 gate R2 real ejercido (p. ej. publicar web EZTI); coste real dentro de presupuesto; memo de copacker en tu mesa.

### F2 — Escala controlada (semanas 6-12)
- APP 2 (idea→prototipo) con 1-2 ideas de tu lista F18 — WIP limit 2 sigue
- Música (APP 4) y Hotel (APP 5) a capacidad sobrante
- **Revisión de capacidad con datos** del ledger → regla pre-fijada de §5 para Max/API
- **Relajación de autonomía** (tu condición B4): tras 4 semanas sin incidentes R2+, tú puedes ampliar la allowlist por ADR — propuesta la trae la retro, decides tú
- Decidir borrado definitivo de `openclaw-core` y clasificación de `kaikuv1`

**Criterio de salida F2:** 1 prototipo interno desplegado; fabricante EZTI elegido; decisión de plan tomada con números.

### F3 — Consolidación (meses 4-6)
- Plantilla de dominio nuevo ejercitada (hogar o deportes)
- EZTI post-fabricante: variedades, canales, patrocinios activos
- Poda: roles/skills sin uso se eliminan (la oficina también despide)
- Auditoría completa de trazabilidad + revisión del operating model contra A2 (éxito a 90 días)

## 7. Operación en régimen (tu semana normal desde F1)

- **Diario (≤5 min):** resumen de las 08:00; responder `APRUEBO/RECHAZO` a la cola.
- **Lunes (15-30 min):** informe profundo; reordenar prioridades si quieres (un mensaje basta).
- **Cuando toque:** enviar emails aprobados (outreach), GO/NO-GO de memos, firmar lo que solo tú puedes firmar.
- **Nunca:** microgestionar pasos, revisar cada acción R0/R1, empujar el sistema para que trabaje.

## 8. Presupuesto consolidado (mensual, desde F1)

| Concepto | € nominal | € real |
|---|---|---|
| hermes-core (e2-small + 30 GB) | ~15 | 0 (créditos) |
| kaikuv1 (sin clasificar — decisión tuya en F2) | ~49 | 0 (créditos) — candidato a ahorro |
| Disco openclaw-core (cuarentena) | ~6 | 0 (créditos) |
| Suscripciones (Claude Pro, ChatGPT Plus, Google AI Pro) | ya las pagabas | 0 incremental |
| OpenRouter emergencia (si se activa) | ≤10 prepago | ≤10 |
| **Total incremental real** | | **≈0-10 €/mes** + gates de compra puntuales |

Muy por debajo del techo (100-150 € incremental). Los créditos GCP son la reserva; cuando caduquen, la factura nominal (~70 €/mes con kaikuv1, ~21 €/mes sin él) pasa a real → alarma del ledger 60 días antes si la fecha de caducidad se registra (pídesela a la consola de GCP y me la das cuando quieras).

## 9. Riesgos residuales con respuesta pre-acordada

| Riesgo | Respuesta (ya decidida) |
|---|---|
| Proveedor revoca OAuth de suscripción | Cadena de fallback §5; la oficina degrada, no muere |
| Hermes (proyecto) se rompe/abandona | Todo lo institucional está en git y las skills son estándar abierto → migrable; Plan C en §5 |
| Daemon quema ventanas de suscripción | Skills con presupuesto por tarea; retro lo vigila; regla de §5 para escalar plan |
| Compromiso de la VM | Sin Tier-0 dentro; tokens revocables uno a uno; VM desechable |
| Tú te saturas de gates | Los gates se agrupan en cola diaria; si aún molesta, la relajación B4 de F2 existe para eso |

## 10. Decisiones que quedan EN TU TEJADO (lista cerrada — todo lo demás está decidido)

| # | Decisión | Cuándo | Bloquea |
|---|---|---|---|
| 1 | GO a la shortlist EZTI de 6 (issue #1) | Ya | Borradores personalizados |
| 2 | Ejecutar F0.B en la VM (30-60 min, cuando quieras) | Cuando quieras | Toda la oficina |
| 3 | Nombre definitivo del sistema (candidatos: Mandi, Tartalo — el bot ya se llama así —, Hermes a secas) | Antes de F1 | Naming de repos/servicios |
| 4 | Datos música E13 (alias, contratos, catálogo) | Antes de activar dominio música | APP 4 pública |
| 5 | Custodia de credenciales Instagram/redes EZTI | Antes de publicar APP 3 | Publicación social |
| 6 | Presupuestar asesor alimentario puntual | Antes del primer lote con copacker | Cierre APP 1 |
| 7 | Clasificar `kaikuv1` (¿qué es? ¿se apaga?) | F2 | ~49 €/mes nominales |
| 8 | Borrado definitivo `openclaw-core` | F2 | ~6 €/mes nominales |
| 9 | Caducidad de créditos GCP (dato para el ledger) | Cuando lo tengas | Alarma de presupuesto |
| 10 | "ultracode": qué es (V1a) | Sin prisa | Nada (excluido del diseño) |
