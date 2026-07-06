# 04 — Herramientas, integraciones y routing de modelos

## 1. Núcleo (F0, semanas 1–2)

| Herramienta | Uso | Estado de verificación |
|---|---|---|
| **GitHub** (repos, Issues, PRs) | Tablero, registro formal, código | Verificado (en uso en esta sesión) |
| **Telegram Bot API** | Intake, aprobaciones (`APRUEBO <id>`), alertas, resumen diario | Verificado por ti en iteraciones previas; el gateway se reescribe limpio |
| **Claude Code + Routines** | Sesiones agénticas interactivas y programadas | Verificado (esta sesión corre sobre esa infraestructura) |
| **Búsqueda/lectura web** de Claude Code | Investigación con fuentes | Verificado |
| **Cloudflare** (Pages + DNS de `ezti.net`) | Web pública de EZTI, deploys inmutables con rollback | Dominio confirmado por ti; integración a validar en F0 con un deploy de staging |
| **GCP** (VM nueva, GCS backups) | Capa 24/7 determinista y copias | Cuenta y créditos confirmados por ti |
| **cron/systemd timers** | Scheduling determinista en la VM | Estándar |

## 2. Segunda ola (F1, semanas 3–6)

- **Gmail API** con scopes `gmail.readonly` + `gmail.compose`: el sistema lee correo relevante (filtrado por etiquetas que tú definas) y **crea borradores**; el scope de envío no se concede, así el gate C (no contactar terceros) está garantizado por OAuth, no por promesa. Enviar siempre lo haces tú con un clic.
- **Google Calendar** (lectura/escritura de tu calendario): riesgo bajo, útil para planificación y para el resumen diario. Conector disponible verificado en este entorno.
- **Cloudflare API token scoped** para automatizar deploys de Pages desde CI.
- **healthchecks / GCP Monitoring** para alertas de uptime hacia Telegram.

## 3. Qué NO introducir todavía, y por qué

| Herramienta | Veredicto | Razón |
|---|---|---|
| **n8n** | No | Segundo cerebro de orquestación = dos fuentes de verdad de flujos; ya generó fricción en el pasado. Cron + código determinista + Routines cubren lo mismo con trazabilidad en git. Reevaluar solo si aparecen >10 integraciones webhook que dolerían mantener a mano. |
| **Vector DB / RAG** | No | La KB cabe en decenas de documentos estructurados; grep + índice supera a embeddings a esta escala y no añade infra. Umbral de reevaluación: cuando la búsqueda estructurada falle de forma medible. |
| **CRM** (HubSpot, etc.) | No | `knowledge/ezti/proveedores.md` + Issues aguanta hasta ~50 contactos activos. Un CRM ahora es coste y burocracia. |
| **Notion u otro wiki externo** | No | Crearía una segunda fuente de verdad compitiendo con git. Todo el conocimiento vive en el repo; si algún día necesitas UI bonita, se genera *desde* el repo, no al revés. |
| **Frameworks multiagente** (LangChain/CrewAI/AutoGen) | No | La topología elegida se implementa con Claude Code + estado en git. Un framework añadiría abstracciones opacas justo donde tú exiges trazabilidad. |
| **Publicación automática en redes** | No (y además gated) | B4(b) exige aprobación humana; una herramienta de autopost sería un arma cargada apuntando a tu marca. Los posts se preparan como borradores en cola de aprobación. |
| **Pasarelas de pago / banca abierta** | No | Colinda con Tier-0. La tienda actual de EZTI ya cobra; no se toca su flujo de dinero en F0–F2. |
| **NVIDIA NIM / modelos locales** | No | Sin máquina 24/7 local y sin capacidad verificada; coste de verificación > beneficio actual. |

## 4. Routing de modelos

### Realidad verificada sobre la que se diseña

- Acceso principal: **Claude Pro por suscripción** vía Claude Code. Coste incremental ≈ 0, pero **capacidad limitada por ventanas de uso**: la moneda escasa no son euros, son ventanas de modelo premium. El ledger las trata como segunda divisa (doc 06).
- ChatGPT Plus y Google AI Pro son suscripciones de chat: valen como **segunda opinión manual tuya**, no como piezas programáticas del sistema.
- Créditos GCP: *podrían* habilitar Gemini vía Vertex AI como capacidad programática de bajo coste real. **No verificado** → tarea de verificación V2 en F0; hasta entonces no forma parte del diseño.

### Política por tipo de trabajo

| Nivel | Trabajo | Modelo | Justificación |
|---|---|---|---|
| 0 | Scheduling, gateway, ledger, parsing, healthchecks, backups | **Ninguno (código determinista)** | Todo lo que no requiere juicio no debe gastar ni un token. Es la decisión de routing más rentable del sistema. |
| 1 | Formateo, resúmenes mecánicos, clasificación de intake, triaje de logs | **Haiku** | Barato y suficiente; fallar aquí es barato de corregir. |
| 2 | Investigación, borradores, implementación rutinaria sobre spec clara | **Sonnet** | Equilibrio calidad/consumo para el grueso del trabajo. |
| 3 | Arquitectura, specs y memos de decisión, revisión QA de código crítico, análisis legal/compliance, redacción final de piezas públicas, todo lo R2+ | **Fable 5** (el mejor disponible bajo tu plan) | Aquí el coste del error supera con mucho el coste del token; tu propio orden G20 (calidad > coste) lo exige. |

Reglas operativas: el nivel lo fija el **tipo de tarea, no el agente** (un mismo rol puede correr en niveles distintos según encargo); ante duda entre niveles, se sube — el sobrecoste de subir es lineal, el de bajar puede ser un error público; si una ventana premium se agota a mitad de encargo crítico, el encargo **se pausa y se reanuda**, nunca se degrada en silencio a un modelo menor (el ledger lo registraría como incidencia).

### Recomendación explícita: Fable 5 + "ultracode"

1. **Fable 5: sí, como cerebro de decisión, no como obrero universal.** Es el modelo correcto para orquestación compleja, arquitectura, revisión y todo lo irreversible. Usarlo para formatear tablas o mover archivos sería quemar la divisa más escasa del sistema. La política de arriba lo implementa.
2. **"ultracode": excluido del diseño hasta verificación.** No me consta como producto o modo verificable de Anthropic, y tú mismo lo has marcado como no confirmado. Ninguna pieza crítica depende de él. Si resulta corresponder a una capacidad real (p. ej. un nivel superior de razonamiento/cómputo bajo tu plan), su hueco natural ya está reservado: se enchufaría como "nivel 3+" para picos puntuales — decisiones de arquitectura fundacionales y revisiones de release — nunca como modo por defecto. Tarea V1 del roadmap: identificar qué es exactamente, sus límites y su forma de acceso, y solo entonces decidir.
3. **Riesgo señalado sin suavizar:** con Claude Pro, la capacidad de nivel 3 puede quedarse corta cuando la oficina esté a pleno rendimiento (F2). No lo resuelvas hoy: el ledger medirá cuántas veces al mes chocas con límites y cuánto trabajo se pausa. Con esos datos, la decisión de subir a un plan superior (o añadir presupuesto API para picos) se toma en la revisión de F2 sobre números reales. Decidirlo hoy sería inventar.

### Fallbacks

Un solo fallback programático candidato: **Gemini vía créditos GCP** (si V2 lo verifica) para trabajo de nivel 1–2 masivo (digestión de documentos largos, extracción). Nunca para nivel 3: la coherencia de las decisiones del sistema debe venir de una sola familia de modelos, o la auditoría de "por qué se decidió esto" se vuelve imposible.
