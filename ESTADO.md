# ESTADO — 2026-07-06 (actualización 2)

**Fase:** F0 (Fundación) en curso · **Pausa:** no · **Gasto real del mes:** 0 €

## Hecho hoy

- Parche correctivo pre-F0 (ADR-002) + ADR-001; estructura completa del repo de gobierno.
- Servicios deterministas escritos y verificados en CI local; **test del kill switch en verde**.
- `infra/`: bootstrap, compose y runbook de VM con las 5 precondiciones.
- **Bot de Telegram creado por el propietario: @Tartaloagentbot** ([#3](https://github.com/lazpiurantxon-bot/kaikhermes/issues/3)). Token recibido (NO almacenado en el repo). Verificación `getMe` **bloqueada desde la sesión**: la política de red del entorno deniega `api.telegram.org` — se verifica al desplegar en la VM, o antes si el propietario permite el dominio en el entorno o verifica en local.
- **EZTI Sprint 1 avanzado** ([#1](https://github.com/lazpiurantxon-bot/kaikhermes/issues/1)): 14 candidatos (v0.2), **6 priorizados** para primera oleada (Pouch Alliance, Sport Foods Labs, Monopacker, Allpack-Stick, Envasados a Terceros, MillMax); dossier de compliance ampliado con **hallazgo nuevo**: restricción de monodosis de plástico en HORECA (ago-2026, impacto probable bajo para EZTI) y obligación RAP de envases RD 1055/2022 (**confirmar inscripción de EZTI**).

## Esperando al propietario

| Qué | Issue | Detalle |
|---|---|---|
| Precondiciones de VM | [#2](https://github.com/lazpiurantxon-bot/kaikhermes/issues/2) | Snapshot probado, inventario, coste — requiere GCP |
| Chat ID + vía de verificación del bot | [#3](https://github.com/lazpiurantxon-bot/kaikhermes/issues/3) | Enviar un mensaje a @Tartaloagentbot; decidir opción (a) dominio permitido, (b) verificación local, (c) al deploy. Recomendado: regenerar token en el deploy |
| Verificaciones V1–V3 | [#4](https://github.com/lazpiurantxon-bot/kaikhermes/issues/4) | ultracode, límites Fable 5, Vertex, Routines |
| **GO a la shortlist de 6** | [#1](https://github.com/lazpiurantxon-bot/kaikhermes/issues/1) | Con tu GO: verifico emails, personalizo los 6 borradores y te los entrego listos para enviar (envío = tuyo, R3) |

## Próximo (sin dependencias)

Verificación de fichas/emails de los 6 priorizados y personalización de borradores (queda listo para tu gate en cuanto confirmes la lista).
