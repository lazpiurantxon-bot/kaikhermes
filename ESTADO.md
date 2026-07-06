# ESTADO — 2026-07-06 (actualización 3 — PIVOTE A HERMES)

**Fase:** F0 replanteada por ADR-003 · **Pausa:** no · **Gasto real del mes:** 0 €

## Decisión del día (ADR-003)

**El sustrato de la oficina es Hermes Agent de Nous Research**, no servicios propios. Corrección doble del propietario aceptada y verificada: (1) el sistema debe basarse en el software Hermes Agent; (2) Hermes SÍ acepta suscripciones como backend (Anthropic OAuth — doc cita Max, verificar Pro—, OpenAI Codex OAuth, Vertex AI con service account). Arquitectura completa en `operating-model/09-arquitectura-hermes.md`.

## Hecho hoy

- ADR-003 + doc 09 (arquitectura de la oficina Hermes: topología, memoria en dos niveles, gobernanza R0–R3 sobre mecanismos nativos, política de backends, clean-room aplicado a Hermes, plan de validación §8, F0 revisado §9).
- `services/` Python **retirados** → `archive/pre-hermes-services/` (no se despliegan; solo referencia).
- `infra/bootstrap.sh` y `runbook-vm.md` reescritos para instalación limpia de Hermes.
- Se conserva todo lo portable: gobernanza, roster de roles, playbooks, pipeline, investigación EZTI completa, precondiciones de VM.

## Esperando al propietario

| Qué | Issue | Detalle |
|---|---|---|
| Precondiciones de VM | [#2](https://github.com/lazpiurantxon-bot/kaikhermes/issues/2) | Sin cambios: snapshot probado, inventario, coste — requiere GCP (Paso 0 de Cloud Shell pendiente) |
| Instalación Hermes | [#5](https://github.com/lazpiurantxon-bot/kaikhermes/issues/5) | Depende de #2; incluye plan de validación §8 |
| Bot / gateway | [#3](https://github.com/lazpiurantxon-bot/kaikhermes/issues/3) | @Tartaloagentbot pasa a ser el canal del gateway nativo de Hermes; regenerar token en deploy |
| Verificaciones | [#4](https://github.com/lazpiurantxon-bot/kaikhermes/issues/4) | Actualizadas: V4 (Anthropic OAuth con Pro) y V5 (control de gasto nativo de Hermes) |
| **GO a shortlist EZTI de 6** | [#1](https://github.com/lazpiurantxon-bot/kaikhermes/issues/1) | Independiente del pivote — puede avanzar YA |

## Nota

El Sprint 1 de EZTI no depende del sustrato: la investigación está en el repo y la retomará el JdG-Hermes al arrancar (doc 09 §9.7). Tu GO a la shortlist sigue siendo lo único que bloquea los borradores personalizados.
