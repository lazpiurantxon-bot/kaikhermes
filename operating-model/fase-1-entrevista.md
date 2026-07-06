# FASE 1 — Entrevista de descubrimiento

**Proyecto:** Operating model multiagente (evolución clean-room inspirada en Hermes Agent / Nous Research)
**Modo de trabajo:** clean-room total. No se ha leído, listado ni analizado ningún archivo, prompt, memoria, skill o artefacto del sistema anterior. Este directorio (`operating-model/`) es nuevo y es el único punto de escritura de esta fase.
**Estado:** esperando respuestas del propietario. No se diseña nada hasta cerrar los bloqueantes.

---

## Cómo responder

Cada pregunta tiene un código (A1, B4…). Puedes responder en un solo mensaje, por código, en el orden que quieras. Las preguntas están en tres niveles:

- **[B]** Bloqueante sin default — son hechos de tu realidad que no puedo inventar. Sin esto no diseño.
- **[B+D]** Bloqueante con default propuesto — es decisión tuya, pero propongo un default; si respondes "defaults OK", aplico el default y queda cerrado.
- **[ND]** No bloqueante — tiene default razonable; puedes corregirlo ahora o después sin romper la arquitectura.

---

## BLOQUE A — Objetivos, proyectos y horizonte

**A1 [B]** ¿Cuáles son los 1–3 proyectos concretos que quieres que el sistema empuje en los primeros 90 días? Nómbralos por dominio (hotel / música / emprendimiento), con su estado actual (idea, en curso, ya en producción) y qué te falta hoy para avanzarlos. Esta es la pregunta que más condiciona todo: sin proyectos reales, la sección de aplicaciones personalizadas sería genérica, y eso lo has prohibido.

**A2 [B]** Definición de éxito medible: ¿qué tiene que haber pasado a los 90 días y a los 12 meses para que digas "esto ha funcionado"? Ejemplos del tipo de respuesta útil: "X € de ingresos nuevos", "N lanzamientos musicales publicados", "1 producto con usuarios reales", "me he quitado Y horas/semana de trabajo operativo".

**A3 [B+D]** Urgencia: ¿necesitas que el sistema produzca valor real en ~2 semanas (arranque mínimo viable, escalar después) o aceptas 4–8 semanas de construcción para arrancar con más piezas montadas?
*Default propuesto: arranque mínimo con valor en 2 semanas; el roadmap escala por fases.*

## BLOQUE B — Autoridad delegada y aprobaciones

**B4 [B+D]** Marca qué puede hacer el sistema **sin pedirte permiso**:
- (a) gastar en APIs/servicios dentro de un límite mensual
- (b) publicar contenido público bajo tu nombre/marca (posts, webs, notas de lanzamiento)
- (c) enviar correos o mensajes a terceros reales
- (d) desplegar a producción servicios **sin** usuarios reales (demos, herramientas internas)
- (e) desplegar a producción servicios **con** usuarios/clientes reales
- (f) crear repositorios e infraestructura nueva
- (g) comprar dominios, suscripciones o servicios de pago

*Default propuesto: sí a (a) con límite, (d) y (f); todo lo demás requiere tu aprobación explícita. Nada público, nada dirigido a terceros y ningún gasto nuevo sin gate humano al principio.*

**B5 [B+D]** ¿Canal principal para aprobar y revisar? (PRs de GitHub, Telegram/WhatsApp, email, Notion, sesiones directas de Claude Code). ¿Y con qué frecuencia quieres resumen ejecutivo: diario, 2–3 por semana, semanal?
*Default propuesto: PRs de GitHub como registro formal de cambios + un canal de mensajería para aprobaciones rápidas; resumen ejecutivo 2–3 veces por semana.*

## BLOQUE C — Presupuesto y acceso a modelos

**C6 [B]** Presupuesto mensual total todo incluido (tokens/planes de Claude + infra + SaaS): ¿<100 € / 100–300 € / 300–1.000 € / >1.000 €? Este número cambia la topología: no diseño lo mismo para 100 € que para 1.000 €.

**C7 [B]** ¿Cómo pagas Claude hoy: plan de suscripción (¿cuál?) o API key de pago por uso? Y cuando dices **"ultracode"**, confirma a qué te refieres exactamente (¿un modo/plan concreto de Claude Code, razonamiento extendido, otra cosa?). No quiero basar la política de routing de modelos en una capacidad que no hayamos verificado los dos.

**C8 [B+D]** Límite de gasto por experimento/iniciativa individual sin permiso adicional.
*Default propuesto: 20–30 € por experimento; por encima, aprobación tuya.*

## BLOQUE D — Stack, hosting e infraestructura

**D9 [B]** Inventario real actual: ¿tienes ya VPS (proveedor y tamaño), cuentas cloud, dominios, máquina local que pueda estar encendida 24/7, GitHub personal u organización, cuentas SaaS relevantes? Lista lo que existe; no asumiré nada que no confirmes.

**D10 [B+D]** Preferencia de operación: ¿local / VPS / cloud gestionado / híbrido? ¿O me delegas la decisión con tu presupuesto como restricción?
*Default propuesto: híbrido — sesiones de Claude Code para el trabajo agéntico + un VPS pequeño para lo que deba persistir (estado, cron, servicios desplegados).*

**D11 [ND]** Restricciones de stack: ¿algún lenguaje/herramienta prohibido o requerido?
*Default: TypeScript + Python, Postgres, Docker, y libertad de elección justificada por pieza.*

## BLOQUE E — Seguridad, legal y compliance

**E12 [B]** Hotel: ¿cuál es tu rol exacto (propietario, gestor, empleado por cuenta ajena)? ¿El sistema tocaría datos de huéspedes o sistemas del hotel (PMS, channel manager, correo corporativo)? Si eres empleado, hay límites duros sobre qué se puede automatizar con datos y sistemas del empleador, y eso recorta o reenfoca las aplicaciones de este dominio.

**E13 [B]** Música: ¿tienes contratos vigentes (distribuidora, editorial, management, colaboradores) que limiten qué puede publicarse o negociarse en tu nombre? ¿Alias artístico y si está registrado como marca?

**E14 [ND]** ¿Operas como autónomo/empresa en España?
*Default: asumo España y RGPD aplicable; no automatizo nada fiscal ni contractual sin tu confirmación explícita, nunca.*

**E15 [B+D]** Secretos: ¿hay credenciales que NUNCA deban estar al alcance de ningún agente (banca, sistemas corporativos del hotel, cuentas personales)?
*Default propuesto: banca y credenciales del empleador quedan fuera del sistema por diseño; el resto se segmenta por agente y por necesidad.*

## BLOQUE F — Los tres dominios en detalle

**F16 [B]** Hotel: los 2–3 dolores operativos concretos que más tiempo te roban o más dinero cuestan (ejemplos del tipo: pricing/revenue, reputación y reviews, comunicación con huéspedes, turnos, upselling, reporting a propiedad).

**F17 [B]** Música: ¿qué haces exactamente (componer, producir, mezclar, lanzar)? ¿Catálogo actual y cadencia de lanzamientos deseada? ¿Distribuidora y herramientas ya en uso? ¿Objetivo dominante: crecer audiencia, ingresos, o volumen/calidad de catálogo?

**F18 [B]** Emprendimiento: ¿hay ideas o productos ya en marcha? ¿Qué perfil te interesa: SaaS/micro-SaaS, contenido/audiencia, servicios productizados, e-commerce? ¿Y tú programas (y a qué nivel) o el sistema será el único que escriba código?

**F19 [ND]** Idiomas, mercados y audiencias por dominio.
*Default: español como idioma de operación interna; español + inglés para activos públicos; mercado España salvo que digas otra cosa.*

## BLOQUE G — Tolerancias

**G20 [ND]** Ordena estas tres prioridades: coste, velocidad, calidad/cero-errores.
*Default: calidad > coste > velocidad para todo lo público; velocidad > coste para exploración interna descartable.*

**G21 [ND]** Un error público bajo tu marca (dato erróneo publicado, email mal enviado): ¿"asumible, se corrige" o "inaceptable"?
*Default: inaceptable → todo output público pasa gate humano hasta que el sistema acumule track record y tú relajes el gate explícitamente.*

## BLOQUE H — Alcance del sistema

**H22 [B+D]** ¿El sistema debe llegar hasta **operar en producción con usuarios/clientes reales** (soporte, incidencias, guardia básica) o hasta "desplegado y monitorizado, la operación con humanos la decides tú"?
*Default propuesto: hasta desplegado + monitorizado + alertas; operación con terceros reales requiere tu autorización por servicio.*

**H23 [B+D]** ¿Los tres dominios en paralelo desde el día 1, o uno como piloto y luego escalar?
*Default propuesto: un piloto primero (el que elijas en A1), con arquitectura ya preparada para operar líneas en paralelo.*

**H24 [ND]** ¿Los artefactos del nuevo sistema (diseño, specs, wiki) viven en este repositorio (`kaikhermes`, branch designado) o prefieres un repositorio nuevo y limpio para el nuevo sistema?
*Default: esta fase queda aquí porque es el branch asignado; recomendaré repo nuevo para el sistema definitivo y lo justificaré en FASE 2.*

---

## Lo que NO te pregunto (porque es mi trabajo decidirlo)

Topología exacta de agentes, patrón de orquestación, modelo de memoria, formato de specs y backlog, estrategia de QA, elección de observabilidad, convenciones de branches/worktrees, y política de routing de modelos por tarea. Todo eso lo decidiré yo en FASE 2 con justificación, condicionado por tus respuestas — y vendrá marcado en "Decisiones que he tomado por ti" para que puedas vetar.

## Resumen de bloqueantes

- **Sin default (imprescindibles):** A1, A2, C6, C7, D9, E12, E13, F16, F17, F18
- **Con default (di "defaults OK" o corrige):** A3, B4, B5, C8, D10, E15, H22, H23
- **No bloqueantes:** D11, E14, F19, G20, G21, H24
