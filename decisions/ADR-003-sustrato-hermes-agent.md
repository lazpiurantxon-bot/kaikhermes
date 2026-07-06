# ADR-003 — Hermes Agent como sustrato de ejecución de la oficina

- **Fecha:** 2026-07-06
- **Estado:** aceptada (decisión del propietario, correctiva)
- **Nivel:** R2 (cambio de arquitectura fundacional) — aprobada explícitamente por el propietario en sesión

## Contexto

El encargo original decía "basado en Hermes Agent de Nous Research". El diseño de FASE 2 lo interpretó como inspiración conceptual e implementó servicios propios en Python (gateway, ledger, watchdog). El propietario corrigió: el sistema debe **basarse en el software Hermes Agent** (framework autónomo open-source de Nous Research, lanzado 2026-02-25), no en código a medida.

Además, el propietario corrigió una afirmación errónea del diseño: **sí es posible alimentar Hermes con suscripciones**. Verificado en la doc oficial de providers: Anthropic vía OAuth de suscripción (documentado para Claude Max + créditos extra; **verificar si Pro basta**), OpenAI Codex vía device-code OAuth (ChatGPT Plus), GitHub Copilot, xAI, y Vertex AI vía service account (vía legítima para créditos GCP). La suscripción de consumo de Google (AI Pro) queda **descartada por decisión del propietario** por contravenir sus términos de uso.

## Decisión

1. **Hermes Agent es el sustrato de la oficina 24/7** en la VM nueva: daemon persistente con su gateway de mensajería (Telegram), memoria nativa (SQLite+FTS5), skills (estándar agentskills.io), cron y subagentes aislados.
2. **Claude Code queda como capa de arquitectura, construcción crítica y QA externo**, operando sobre la suscripción Claude Pro vía el repo (PRs, revisiones, diseño). No forma parte del daemon.
3. **Se retiran los servicios Python propios** (`services/`) → `archive/pre-hermes-services/` (conservados solo como referencia/rollback; no se despliegan). Sus funciones pasan a las piezas nativas de Hermes. El concepto del ledger de dos divisas se conserva: se implementará **dentro** de Hermes (skill/cron) solo si Hermes no trae control de gasto nativo equivalente (verificación pendiente).
4. **El operating model (docs 00–08) sigue vigente en lo sustantivo** — gobernanza R0–R3, clean-room, roster de roles, pipeline INTAKE→RETRO, aplicaciones, KPIs —; el documento `operating-model/09-arquitectura-hermes.md` define el mapeo al sustrato Hermes y **prevalece sobre 01/04/05 donde entren en conflicto**.
5. **Clean-room reconciliado con "usar Hermes":** instalación NUEVA de Hermes (release estable actual), `~/.hermes` en blanco, workspace nuevo, sin `hermes claw migrate`, sin importar memoria/skills/config del Hermes de la VM antigua. La regla de importación ítem a ítem se mantiene.

## Consecuencias

- F0 se replantea: en lugar de desplegar servicios propios, se instala y configura Hermes (issue #5) tras las precondiciones de VM (#2, sin cambios).
- El bot @Tartaloagentbot se reutiliza como canal del gateway de Hermes (es un bot nuevo, no del sistema anterior — no viola clean-room).
- Se abre un **plan de validación de instalación** (doc 09 §8): lo documentado por Hermes se trata como "por verificar en tu instalación" hasta probarlo — en particular OAuth de Anthropic con plan Pro, granularidad del command approval y gobernanza de skills auto-creadas.
- Los errores corregidos del diseño quedan registrados: (a) malinterpretar "basado en Hermes"; (b) afirmar que las suscripciones no podían alimentar Hermes.

## Addendum 2026-07-06 — el sistema anterior es OpenClaw

El inventario GCP (`knowledge/core/infra-gcp-inventario.md`) confirma que el sistema previo era **OpenClaw** (instancia `openclaw-core`, TERMINATED). Refuerza el clean-room: `hermes claw migrate` (migración desde OpenClaw) queda **prohibido**; el disco de `openclaw-core` no se monta ni se importa. Donde este ADR y el doc 02 dicen "Hermes antiguo", léase "sistema anterior = OpenClaw". Queda por determinar qué corre en `kaikuv1` (RUNNING) antes de decidir repave vs VM nueva.
