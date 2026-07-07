# FASE 1 — Acta de respuestas (contrato de diseño)

**Fecha:** 2026-07-06
**Fuente:** respuestas del propietario a la entrevista de descubrimiento.
**Estatus:** este documento es el registro vinculante de restricciones y prioridades. Cualquier cambio posterior debe registrarse como enmienda datada, no como edición silenciosa.

## A — Objetivos y horizonte

- **Proyectos prioritarios 90 días:** (1) EZTI — gel energético natural (miel, limón, sal), ya en venta vía web y proveedores locales; falta copacker, costes unitarios, MOQ, estabilidad, etiquetado, web/IG, plan comercial y ayudas. (2) Hermes/Mandi — el propio sistema operativo agéntico, clean-room. (3) Música — dominio activo pero sin estructura de negocio; solo trabajo privado hasta aclarar contratos/alias.
- **Hotel:** dominio secundario. El propietario es **empleado (recepcionista)**, no dueño. Objetivo declarado: dejar el empleo para dedicarse a sus emprendimientos. Prohibido tocar datos de huéspedes o sistemas del empleador sin autorización expresa y legalmente válida.
- **Éxito 90 días:** EZTI con fabricante cerrado o primer lote comercial en marcha + primeros patrocinios de atletas locales; Hermes/Mandi estable (contexto, priorización, tareas, borradores, resúmenes, logging, memoria, gates); música con catálogo inventariado, pipeline y 1–2 activos preparados sin publicar.
- **Éxito 12 meses:** EZTI con ventas recurrentes, cumplimiento resuelto, nuevas variedades y equipo deportivo; Hermes/Mandi como capa operativa diaria con departamentos especializados (visión: idea → app + web + material + hojas de ruta de forma autónoma); música con cadencia sostenible, hipótesis de monetización y primeros directos.
- Sin objetivos financieros cerrados: en FASE 2 se permiten rangos por escenario, no cifras inventadas.
- **A3:** arranque mínimo con valor en ~2 semanas; escalar por fases.

## B — Autoridad delegada

- **Sin permiso:** (a) gasto en APIs/servicios dentro de límites; (d) desplegar servicios sin usuarios reales; (f) crear repos/ramas/issues/docs/infra reversible y de bajo coste.
- **Con aprobación explícita:** (b) publicar bajo su marca; (c) mensajes/correos a terceros reales; (e) producción con usuarios reales; (g) compras y pagos recurrentes nuevos.
- Los límites podrán relajarse en el futuro solo con autorización explícita y tras semanas sin errores.
- **Canales:** PRs de GitHub (registro formal) + Telegram (aprobaciones rápidas). Resumen breve diario cuando haya actividad; resumen profundo 2–3/semana o semanal.

## C — Presupuesto y modelos

- **Total mensual:** 100–300 € incluyendo suscripciones e infra. Coste incremental objetivo <100–150 €/mes mientras haya créditos cloud. Salto sostenido >300 €/mes = aprobación explícita.
- **Acceso a Claude:** suscripción **Claude Pro** vía Claude Code/OAuth (no API de pago por uso como fuente principal). También ChatGPT Plus y Google AI Pro. Créditos Google Cloud disponibles. Fallbacks (Gemini, NIM, local) solo sobre capacidades verificadas.
- **"ultracode": NO es capacidad verificada.** Queda marcado pendiente; ninguna política crítica de routing se apoya en él.
- **Por experimento:** 20–30 € sin permiso adicional.
- Nota del propietario: el uso de modelos cubierto por suscripción no genera coste real incremental; ante la duda, pedir aprobación humana.

## D — Infraestructura

- Inventario: VM Google Cloud (Ubuntu 24, disco 100 GB) con instalaciones previas de Hermes **no fiables salvo verificación**; Telegram probado; repo `kaikhermes` con branch designado; dominio `ezti.net` en Cloudflare; suscripciones citadas; créditos GCP; experimentos previos con n8n/contenedores/fallbacks. **No hay máquina local 24/7.**
- Lo previo es contexto histórico, no base fiable.
- **D10:** híbrido — Claude Code para trabajo agéntico; VM pequeña para persistencia/cron/servicios/observabilidad; cloud según coste; local solo pruebas.
- **D11:** TS + Python, Docker, Postgres aceptados; **SQLite preferible en MVPs internos** si reduce complejidad sin perder trazabilidad; evitar sofisticación innecesaria.

## E — Seguridad y legal

- Hotel: empleado; sin acceso a PMS, channel manager, correo corporativo, datos de huéspedes ni documentación interna. Sí: propuestas, checklists, análisis genéricos, productividad personal.
- Música: contratos/alias/marca **sin verificar** → prohibido publicar, negociar, contactar, distribuir o firmar. Permitido: borradores, investigación, organización, activos privados.
- España/Gipuzkoa, RGPD. Nada fiscal/contractual/subvenciones enviadas sin revisión humana.
- **Nunca al alcance de ningún agente:** banca; sistemas y credenciales del empleador; Hacienda con capacidad de presentación; identidad digital crítica; cuentas personales sensibles. Resto: segmentación por agente, necesidad real y mínimo privilegio.

## F — Dominios

- Hotel (dolores): documentación/reporting repetitivo; comunicación y propuestas internas; procesos de recepción (PMS, check-in, lector DNI, TicketBAI, cartelería, limpieza/reporting). Sin automatización sobre datos reales.
- Música: batería con años de experiencia, interés en producción y productos musicales. Prioridad: calidad/catálogo y estructura antes que publicación.
- Emprendimiento: EZTI (principal); Hermes/Mandi; IoT stock bar/restaurante; agente CAM/CNC desde STEP; app musical tipo TP-7; app productividad "Sísifo"; impresión 3D; playlists para establecimientos; publicidad local; servicios productizados. Preferencia: validación rápida, B2B o físico/SaaS. El propietario tiene base técnica y puede operar/probar; los agentes escribirán la mayor parte del código.
- Idiomas: interno español; públicos ES/EU/EN; mercado España/País Vasco/Europa según proyecto.

## G — Tolerancias

- Público/legal/marca/terceros/producción: calidad > coste > velocidad. Exploración interna reversible: velocidad > coste. Arquitectura base de Hermes: calidad > velocidad > coste.
- Error público bajo su marca: **inaceptable** → gate humano en todo output público hasta relajación explícita.

## H — Alcance

- Hasta desplegado + monitorizado + alertas. Operar de cara a terceros reales: autorización específica por servicio.
- Piloto técnico: Hermes/Mandi. Piloto de negocio: EZTI. Hotel y música secundarios. Arquitectura preparada para dominios futuros (p. ej. hogar, deportes).
- Artefactos de esta fase en este repo/branch; en FASE 2, recomendación explícita y razonada sobre repo definitivo (no decidir por inercia).

---

## Enmienda E1 — Oficina autónoma de departamentos (2026-07-07)

**Fuente:** instrucción directa del propietario en sesión (encargo de la oficina autónoma). **Registrada como enmienda datada según la regla de cabecera de este acta.** Diseño resultante: ADR-004 y `operating-model/10-oficina-autonoma.md`.

Nueva autoridad delegada (amplía B; no toca C, E ni G):

- **(h) Trabajo proactivo sin encargo.** Los departamentos de la oficina (análisis de mercado, desarrollo de producto, campañas de marketing, estudio de marca) generan y adelantan trabajo por iniciativa propia, con cadencias y límites WIP configurados. Todo queda registrado y es vetable retroactivamente.
- **(i) Marcas nuevas de oficina.** La oficina puede **crear marcas nuevas** y **publicar/operar en su nombre de forma autónoma** (R1 con compliance embebido y registro visible), incluida la apertura de cuentas y web propias de esas marcas.

Límites que esta enmienda **no** relaja (siguen a rajatabla):

1. **Nada en nombre de las marcas/proyectos existentes del propietario** (EZTI, música, hotel, el propio sistema, y cualquier proyecto ya en desarrollo): publicar, desplegar o modificar en su nombre sigue siendo R2/R3 con gate — la oficina solo prepara propuestas y borradores. Música y hotel siguen **prohibidos** para toda acción externa (E, sin cambios).
2. **Contacto con terceros reales:** gate R3 individual siempre, también bajo marcas de oficina (B/c, sin cambios).
3. **Gasto:** límites de C sin cambios (≤20-30 €/tarea autónomo; recurrente → gate).
4. **Separación de identidad:** una marca de oficina no se presenta públicamente como vinculada al propietario ni a sus marcas existentes; esa asociación es decisión R2 suya.
5. La aplicación de estos límites es **determinista y fail-closed** (registro de marcas + `oficina politica check`); marca sin registrar = protegida.
