# 00 — Resumen ejecutivo

## Qué se ha diseñado

Una **oficina agéntica** ("Mandi", nombre de trabajo — ver preguntas abiertas) que opera tus proyectos por líneas de dominio (EZTI, Hermes-core, Música, Hotel, y dominios futuros) bajo tu supervisión, con autonomía real en lo interno y reversible, y gate humano obligatorio en todo lo público, externo o irreversible.

## Las cinco decisiones que definen el sistema

1. **Estado durable, cómputo efímero.** La "oficina" no es una flota de agentes corriendo 24/7 (tu plan Claude Pro no lo soporta y no lo necesita). La continuidad vive en **git + GitHub Issues** (specs, decisiones, conocimiento, tablero); los agentes son **sesiones de Claude Code** (interactivas o programadas) que hidratan estado, trabajan y escriben estado de vuelta. La capa que sí corre 24/7 en la VM es **código determinista sin LLM**: gateway de Telegram, scheduler, ledger de gasto, watchdog.

2. **Topología: híbrido jerárquico ligero.** Un Orquestador (Jefe de Gabinete) que prioriza, descompone y enruta pero no hace trabajo especializado; especialistas **efímeros** por encargo (Investigación, Estrategia, Constructor, QA, SRE, Documentalista); dos roles transversales con cadencia fija (Contralor de gasto — determinista; Retro semanal). QA siempre en contexto separado del Constructor. Se rechazan: jerarquía de managers (sobredimensionada), swarm sin ownership, y monolito de un solo agente (contaminación de contexto entre dominios).

3. **Clean-room verificable.** Hecho verificado: `kaikhermes` estaba **vacío** al iniciar (primer commit = root commit) → es clean-room de facto y se queda como **repo de gobierno**. Alcance honesto de la garantía: cubre **artefactos y proceso** (repo verificable por root commit + proceso declarado de no-lectura/no-importación), no el conocimiento previo que personas o modelos conserven. La VM antigua se pone en **cuarentena** (snapshot + parada de servicios) y se levanta **VM nueva** desde un bootstrap script versionado. Nada del sistema anterior entra sin tu autorización escrita ítem a ítem. Secretos en dos niveles: Tier-0 (banca, empleador, Hacienda, identidad — **nunca** en el sistema) y Tier-1 (tokens con alcance mínimo, segmentados por servicio).

4. **Gobernanza por niveles de riesgo R0–R3.** R0/R1 (interno, reversible / infra interna): autónomo con log. R2 (contenido público, prod sin usuarios reales fuera de allowlist, gasto en umbral): aprobación por Telegram (`APRUEBO <id>`). R3 (terceros reales, producción con usuarios, gasto recurrente, legal): aprobación + registro en PR. Prohibido por defecto: dominios Tier-0, presentación fiscal, firma de contratos, sistemas del hotel, publicación musical (hasta resolver contratos/alias).

5. **Routing de modelos honesto con tu plan.** Fable 5 (o el mejor disponible bajo Pro) reservado para arquitectura, specs, revisión y decisiones; Sonnet para construcción rutinaria e investigación; Haiku para transformaciones mecánicas; **código determinista para todo lo que no requiere juicio**. "ultracode" queda **excluido del diseño hasta verificación** — no me consta como producto/modo real y tú mismo lo has marcado como no verificado. La capacidad premium de Pro es el recurso escaso: se raciona, se mide, y la decisión de subir a Max se toma en la fase 2 del roadmap **con datos de uso**, no por intuición.

## Qué produce en 2 semanas (F0)

- Loop de trabajo operativo: intake por Telegram → tablero en GitHub Issues → resumen diario → aprobaciones por Telegram.
- **EZTI Sprint 1:** shortlist calificada de copackers (MOQ, costes, certificaciones), primer dossier de **compliance alimentario** (etiquetado UE 1169/2011, claims 1924/2006, RGSEAA) con avisos de verificación profesional — TicketBAI y facturación son un módulo fiscal separado y posterior, de operación comercial —, y borradores de contacto listos para tu aprobación.
- VM nueva operativa con gateway, ledger y backups.

## Qué NO va a hacer este sistema (y por qué lo digo sin suavizar)

Tu visión a 12 meses incluye "genera contratos e implicaciones legales automáticamente" e "ingresos pasivos sin que yo haga nada". Lo primero es **borradores sí, validez legal no**: ningún sistema debe firmar ni presentar nada en tu nombre, y los documentos legales/fiscales salen siempre marcados para revisión profesional. Lo segundo es un objetivo direccional legítimo, pero el mecanismo real es: el sistema comprime tu trabajo hasta dejarte solo **decisiones y firmas**; "cero intervención" con dinero real de por medio es incompatible con la gobernanza que tú mismo has exigido (G21: error público inaceptable). El diseño te acerca a esa visión por el camino que no explota.

## Índice de documentos

| Doc | Contenido |
|---|---|
| `fase-1-entrevista.md` / `fase-1-respuestas.md` | Entrevista y acta vinculante |
| `01-arquitectura-topologia-agentes.md` | Arquitectura objetivo, topología, roster completo de agentes |
| `02-clean-room-aislamiento-seguridad.md` | Perfiles, workspaces, VM, secretos, checkpoints |
| `03-memoria-skills-conocimiento.md` | Memoria, skills con gobernanza, knowledge base |
| `04-herramientas-integraciones-modelos.md` | Herramientas núcleo, qué no introducir aún, routing de modelos, Fable 5 + ultracode |
| `05-operating-model-ejecucion.md` | Pipeline idea→producto, QA, despliegue, monitorización |
| `06-gobernanza-costes-rollback.md` | R0–R3, aprobaciones, ledger, circuit breakers, rollback |
| `07-aplicaciones-personalizadas.md` | 5 aplicaciones end-to-end (EZTI ×2, Hermes, Música, Hotel) |
| `08-roadmap-riesgos-decisiones.md` | Roadmap F0–F3, riesgos, decisiones tomadas por ti, preguntas abiertas |
