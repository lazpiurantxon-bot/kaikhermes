# 08 — Roadmap, riesgos, decisiones tomadas y preguntas abiertas

## 1. Roadmap por fases

### F0 — Fundación (semanas 1–2) → valor real en 2 semanas (A3)

Infraestructura mínima + primer resultado de negocio en paralelo, no en serie:

1. Estructura del repo de gobierno: `domains/`, `knowledge/`, `decisions/`, `playbooks/`, `skills/`, `infra/`, `ESTADO.md`; playbooks de dominio (EZTI, core, música, hotel) con sus límites legales embebidos.
2. VM nueva desde `infra/bootstrap.sh`; VM antigua a cuarentena (snapshot + stop). 
3. `gateway-telegram` v1: intake, cola de aprobaciones (`APRUEBO/RECHAZO/PREGUNTA`), alertas, kill switch (`PARA TODO`) — probado.
4. Ledger v1 (SQLite): gasto real + eventos de rate-limit; circuit breakers básicos.
5. Convenciones del tablero en GitHub Issues + resumen diario.
6. **EZTI Sprint 1 (APP 1):** shortlist de copackers v1 + dossier normativo v1 + borradores de contacto en tu cola de aprobación.
7. Verificaciones **V1** (qué es "ultracode", límites reales de Fable 5 bajo Pro) y **V2** (¿créditos GCP cubren Vertex/Gemini?).

**Criterio de éxito F0:** apruebas tu primer gate real por Telegram y tienes en la mano una shortlist de fabricantes que no existía hace dos semanas.

### F1 — Oficina operativa (semanas 3–6)

Pipeline completo INTAKE→RETRO con QA activo; APP 1 completada (modelo de costes por escenario + barrido de ayudas); APP 3 hasta staging (web EZTI + kit de patrocinio); Gmail (readonly+compose) y Calendar; primera retro semanal y primeras skills propuestas; runbooks de deploy y rollback probados.

### F2 — Escala controlada (semanas 7–12)

APP 2 en marcha con 1–2 ideas reales de tu lista F18 pasando el pipeline completo; APP 4 (música privada) y APP 5 (hotel/plan de salida) a prioridad baja; revisión de capacidad **con datos del ledger** → decisión informada: mantener Pro / subir de plan / presupuesto API para picos; primera auditoría de la cadena de trazabilidad; propuesta de relajación de límites solo si hay semanas sin errores (tu condición B4).

### F3 — Consolidación (meses 4–6)

Plantilla de "nuevo dominio" ejercitada (hogar o deportes como prueba de H23); operación comercial de EZTI ampliada (post-fabricante: variedades, canales); evaluación honesta: qué agentes/roles ganaron su sitio y cuáles se eliminan (la oficina también despide); revisión completa del operating model contra resultados de 90 días (A2).

## 2. Riesgos y trade-offs principales

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Capacidad de Claude Pro insuficiente** cuando la oficina esté a pleno uso | Trabajo pausado, frustración | Routing por niveles, batching, medición en ledger; decisión de upgrade en F2 con datos |
| **Ejecución programada bajo suscripción**: Routines verificadas en este entorno, pero su alcance/límites exactos para tu cuenta deben confirmarse | El "trabaja mientras duermo" se reduce | Verificación V3 en F0; fallback: sesiones que tú lanzas + capa determinista que sí es 24/7 |
| **Cuello de botella humano** (todos los gates eres tú) | Cola de aprobaciones estancada | Ítems de gate autocontenidos de 3 líneas; lo no aprobado espera sin romper nada; nunca silencio=sí |
| **Alucinación en material regulatorio/legal** | Error caro en EZTI | Fuente primaria obligatoria + flag de verificación profesional + QA de fuentes; el gasto en un asesor alimentario puntual **no** lo sustituye este sistema |
| **Dispersión** (10 ideas de F18 tirando a la vez) | Nada llega a término | WIP limit 2, kill-criteria en BRIEF, prioridad EZTI fijada por acta |
| **Deriva de memoria/skills** | Comportamiento no auditado | Todo cambio de comportamiento = PR con merge humano; sin excepciones |
| **Trade-off asumido: menos autonomía que tu visión de 12 meses** | Más clics tuyos | Es deliberado (G21). La autonomía se gana con track record, está previsto el mecanismo de relajación |
| **Trade-off asumido: sin vector DB/framework multiagente** | Menos "moderno" | Trazabilidad y simplicidad valen más a esta escala; hay umbrales de reevaluación definidos |

## 3. Decisiones que he tomado por ti

1. **Estado durable en git + GitHub Issues; cómputo efímero** — la oficina no es una flota de procesos LLM 24/7; lo permanente es el estado y una capa determinista.
2. **Topología: híbrido jerárquico ligero** (JdG + especialistas efímeros + tablero durable), rechazando jerarquías profundas, swarm y monolito.
3. **QA siempre en contexto separado del Constructor**, con obligación de ejecutar, no solo leer.
4. **`kaikhermes` se queda como repo de gobierno** (verificado vacío = clean-room de facto); un repo por producto. Renombrarlo es cosmético y tuyo.
5. **VM nueva (repave) y cuarentena de la antigua** con snapshot y borrado diferido a tu aprobación.
6. **Capa 24/7 sin LLM** (gateway, ledger, watchdog) — el routing más rentable es no usar modelo donde no hace falta juicio.
7. **GitHub Issues como tablero** en vez de construir un board propio o adoptar Notion/n8n.
8. **Memoria = markdown versionado con gobernanza de PR**; sin vector DB, sin memoria opaca, sin autoaprendizaje sin merge humano.
9. **Gmail limitado por scopes OAuth incapaces de enviar** (readonly + compose): el gate de "no contactar terceros" es técnico, no una promesa.
10. **Niveles de riesgo R0–R3 + lista de prohibidos por defecto**, mapeando exactamente tu B4/E15, con circuit breakers deterministas y kill switch.
11. **Ledger de dos divisas** (€ reales y capacidad de suscripción) como base para decidir upgrade de plan en F2 con datos.
12. **Routing de modelos por tipo de tarea**: determinista → Haiku → Sonnet → Fable 5; ante duda se sube de nivel; nunca degradación silenciosa en trabajo crítico.
13. **"ultracode" excluido del diseño** hasta verificación (V1), con su hueco reservado si resulta real.
14. **WIP limit de 2 iniciativas activas** al arranque.
15. **Prioridad entre apps:** APP 1 (EZTI proveedores) primero, APP 3 después, APP 2 en F2, APP 4 y 5 a capacidad sobrante — deriva de tu propio orden (piloto de negocio = EZTI).
16. **Nombre de trabajo "Mandi"** para el sistema nuevo en rutas y branches (`/srv/mandi`, `mandi/<slug>`), para distinguirlo del Hermes anterior. Cambiarlo es barato ahora, caro después.

## 4. Preguntas que siguen abiertas

1. **Nombre definitivo del sistema** (¿Hermes, Mandi, otro?) — afecta a naming de servicios y repos; decidir antes de F1.
2. **"ultracode" (V1):** qué es exactamente, límites y forma de acceso. Hasta entonces, fuera del diseño.
3. **Límites reales de Fable 5 bajo tu plan Pro (V1):** cuánta capacidad de nivel 3 hay de verdad por semana; lo medirá el ledger.
4. **Créditos GCP → ¿Vertex/Gemini API? (V2):** determina si existe el fallback programático de nivel 1–2.
5. **Alcance real de Routines/sesiones programadas para tu cuenta (V3):** condiciona cuánto trabajo ocurre sin que tú inicies sesión.
6. **Música (E13):** alias, contratos, catálogo real — sin esto, todo lo público del dominio sigue bloqueado; la APP 4 está diseñada precisamente para ponerte esa decisión encima de la mesa.
7. **Credenciales del Instagram/redes de EZTI:** quién las custodia y cómo se instrumenta el gate de publicación (¿borradores en cola y publicas tú, o token gestionado con gate?).
8. **Asesor alimentario/fiscal puntual para EZTI:** el dossier normativo lo prepara el sistema, pero la validación profesional es un gasto pequeño y recomendable antes del primer lote con copacker — ¿lo presupuestamos en F1?
9. **Borrado definitivo de la VM antigua** tras 30 días de cuarentena — requerirá tu aprobación explícita.
10. **Rescate de artefactos del sistema anterior:** por defecto nada entra; si algo merece rescate (p. ej. el bot de Telegram probado), pídelo ítem a ítem por escrito y se evaluará bajo la regla de importación.
