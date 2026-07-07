# 10 — La oficina autónoma: orquestador, departamentos y panel

**Estatus:** vigente (ADR-004, enmienda E1 del acta). Complementa al doc 09
(sustrato Hermes Agent) y prevalece sobre 01/05 en lo relativo a la capa de
oficina. Implementación completa en `office/` y `skills/oficina/` de este repo.

## 1. Qué es

Una oficina de agentes 24/7 **dentro del daemon Hermes Agent**: un
orquestador (el agente raíz) y cuatro departamentos especialistas
(subagentes aislados) que **adelantan trabajo por iniciativa propia** —
análisis de mercado, desarrollo de producto, campañas de marketing y estudio
de marca — sin publicar jamás nada en nombre de las marcas existentes del
propietario, pero con libertad para crear marcas nuevas de oficina y operar
bajo ellas. El propietario la dirige desde Telegram (gateway nativo) y desde
un **panel web propio** que no es un visor: es la mesa de mando.

```
             PROPIETARIO
   Telegram (gateway nativo) · Panel web (127.0.0.1:8787, túnel SSH)
        │ intake / APRUEBO-RECHAZO / pausas / kill        │
┌───────▼──────────────────────────────────────────────────▼──────┐
│ HERMES AGENT (daemon 24/7 en hermes-core)                       │
│                                                                  │
│  ORQUESTADOR (agente raíz, skill orquestador-despacho)           │
│  cron cada 15 min + al llegar mensaje:                           │
│  triaje intake → despacho → pulsos → gates → mantenimiento       │
│        │ spawn subagentes aislados (primitiva nativa)            │
│  ┌─────┴─────┬───────────┬────────────┬───────────┐              │
│  │ MERCADO   │ PRODUCTO  │ MARKETING  │ MARCA     │  + roles     │
│  │ análisis  │ idea→memo │ campañas   │ rebrand + │  semilla     │
│  │ proactivo │ →prototipo│ y piezas   │ marcas    │  (QA, doc…)  │
│  └─────┬─────┴─────┬─────┴─────┬──────┴─────┬─────┘              │
└────────┼───────────┼───────────┼────────────┼────────────────────┘
         ▼           ▼           ▼            ▼
   TABLERO ~/office/state  (JSON auditable; CLI `oficina`, determinista:
   estados, WIP, política de marcas fail-closed, breakers, ledger, feed)
         ▲
   PANEL WEB (FastAPI+UI, systemd) — lee/escribe el mismo tablero
   REPO kaikhermes — lo institucional sigue llegando vía PR (doc 09 §3)
```

## 2. El orquestador

El JdG del doc 01, encarnado en el agente raíz de Hermes con la skill
`orquestador-despacho`. **Todo input del propietario pasa por él** (Telegram
o panel → bandeja `intake` del tablero) y él decide: responder directamente,
rechazar (prohibidos), pedir aclaración, o convertirlo en tareas asignadas a
departamentos con prioridad, riesgo y marca declarados. Además: despacha la
cola a subagentes según WIP, lanza los pulsos proactivos vencidos, retoma los
gates decididos y mantiene el tablero limpio. Corre por cron cada 15 min y al
llegar cualquier mensaje; un ciclo sin trabajo cuesta segundos.

## 3. Los departamentos (proactivos por diseño)

| Dept | Misión | Pulso por defecto | Skills que reutiliza |
|---|---|---|---|
| `mercado` | vigilancia de mercado/competidores, radar de oportunidades, ayudas | 24 h | rol-investigacion, rol-documentalista |
| `producto` | idea → brief → memo go/no-go → spec → prototipo interno | 12 h | rol-estratega, rol-constructor, rol-qa |
| `marketing` | campañas: posicionamiento, calendario, piezas, publicación | 24 h | ezti-claims (checklist), outreach-r3 |
| `marca` | dossiers de rebranding (solo propuesta) + marcas nuevas de oficina | 48 h | rol-estratega, rol-investigacion |

El **pulso** es el mecanismo de proactividad: el orquestador consulta
`oficina pulso pendientes` (determinista: cadencia vencida + hueco de
backlog + sin pausas) y lanza el subagente del departamento en modo PULSO,
que genera o avanza trabajo él solo. Las cadencias, WIP y backlog objetivo se
ajustan desde el panel sin tocar cron ni código. Los departamentos se piden
cosas entre sí dejando tareas en cola (p. ej. producto pide naming a marca).

## 4. La frontera de marcas (la regla del encargo)

Registro en el tablero (`marcas.json`) con dos clases:

- **Protegidas** (seed: `ezti`, `musica`, `hotel`, `hermes-core` — y las que
  el propietario añada): la oficina puede investigar, redactar y **proponer**
  (dossiers, borradores, staging), pero publicar/desplegar/modificar en su
  nombre → **gate R2/R3 siempre**; para `musica` y `hotel` ni siquiera hay
  gate (deny, acta E).
- **De oficina** (las crea `dep-marca`): los departamentos pueden operar y
  **publicar de forma autónoma** (R1) bajo ellas, con checklist de compliance
  embebido, registro en el feed y mención en el resumen diario (veto
  retroactivo). Identidad separada: jamás se presentan como vinculadas al
  propietario o a sus marcas.

Aplicación en tres barreras (doc 09 §4): (1) material — las credenciales de
marcas protegidas no existen en la VM; (2) determinista — `oficina politica
check` (exit 0/3/4 = allow/gate/deny), fail-closed ante marca desconocida,
probado en `office/tests/test_policy.py`; (3) skills — el procedimiento de
cada departamento repite la regla. Contactos con terceros y gasto siguen las
reglas de siempre (R3 / límites del acta C).

## 5. El panel (interfaz de mando)

`office/panel/` — servicio systemd de usuario, `127.0.0.1:8787`, token de
propietario, acceso por túnel SSH. No contiene agencia: escribe el tablero
por el mismo camino que los agentes. Qué permite:

- **Usar**: caja de intake al orquestador (con prioridad); crear tareas ya
  asignadas; notas a cualquier tarea (los agentes las leen como órdenes).
- **Orquestar**: decidir gates (APRUEBO/RECHAZO con nota); asignar/recolar/
  archivar/cerrar tareas; reordenar prioridades; pausar/reanudar
  departamentos; **pulso ahora**; ajustar cadencias, WIP y presupuesto.
- **Supervisar**: tablero kanban (intake→cola→en curso→gate→revisión→hecha),
  agentes en trabajo con tiempos, cola de gates, registro de marcas, ledger
  de gasto con freeze, feed de actividad completo, breakers.
- **Parar**: pausa global y kill switch (rearme solo del propietario), además
  de los kill switches del sustrato (`systemctl stop hermes`, «PARA TODO»).

## 6. Ciclos de ejemplo (de punta a punta)

**Proactivo:** cron 08:15 → despacho → pulso de `marca` vencido → subagente
propone la marca nueva "zephyr" para el prototipo sin nombre de producto →
`oficina marca crear` (R1, evento) → siguiente pulso de `marketing` → campaña
para zephyr → `politica check publish zephyr` = ALLOW → compliance → publica
→ feed + resumen diario de las 08:00 siguientes. El propietario lo ve, y si
no le gusta: retira o protege la marca desde el panel.

**Input del propietario:** escribe en el panel «prepara un rebranding de
EZTI» → intake → despacho: triaje → tarea a `marca` con `--marca ezti`,
riesgo R2 → subagente prepara el dossier (2-3 direcciones, maquetas, plan de
migración con rollback) → `politica check modify_protected ezti` = GATE →
entrega + gate `proposal` → el propietario ve el dossier en el panel y decide.
Nada tocó EZTI real en ningún paso.

## 7. Operación y salvaguardas

- WIP global 2 (tablero §5), WIP 1 por departamento, backlog objetivo por
  departamento — el CLI los aplica, no hay que vigilarlos.
- Breakers deterministas: 3 fallos seguidos → departamento en pausa; ≥80% del
  presupuesto → freeze de gasto; kill switch → los agentes no pueden mutar el
  tablero. Rearmes: solo propietario.
- Retro semanal (skill 10) audita además la oficina: diffs de skills,
  muestreo de acciones externas vs `politica check`, publicaciones autónomas.
- El tablero es estado **operativo** (respaldable con el backup de la VM);
  lo institucional sigue el camino de siempre: PR al repo.
- Todo lo dependiente de la versión de Hermes está marcado **[TBV]** en
  `office/hermes/instalacion.md` y se verifica en la VM (issue #5).
