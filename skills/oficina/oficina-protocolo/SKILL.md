---
name: oficina-protocolo
description: Protocolo común de la oficina autónoma — cómo todo agente (orquestador o subagente de departamento) usa el tablero con el CLI `oficina`, respeta la política de marcas y los controles del propietario. Cargar SIEMPRE junto a cualquier skill de departamento u orquestación.
---

# Protocolo de la oficina

Eres parte de la oficina autónoma que corre sobre Hermes Agent. El tablero
vive en `~/office/state/` y se opera **solo** con el CLI `oficina` (está en el
PATH). Nunca edites los JSON del tablero a mano.

## 0. Antes de nada, en cada sesión

1. `oficina estado` — lee control, colas, gates y pulsos. Si `kill` o
   `pausa_global` están activos: **no trabajes**; termina informando.
2. Carga el playbook del dominio afectado (`domains/<dominio>/playbook.md`) y
   recuerda el acta (`operating-model/fase-1-respuestas.md`, enmienda E1).

## 1. Ciclo de vida de una tarea (estados)

`intake → queued → running → review → done`, con desvíos a `gate` (esperando
al propietario), `blocked` (fallo) y `archived` (matada; matar pronto es éxito).

- Tomar trabajo: `oficina tarea empezar T-0042 --por <tu-nombre>` — el CLI
  aplica WIP y pausas; si te lo niega, **no insistas**: pasa a otra cosa.
- Entregar: `oficina tarea entregar T-0042 --resultado "<qué hay y dónde>"`
  y registra artefactos: `oficina tarea artefacto T-0042 --ref <ruta/PR/URL> --tipo doc`.
- Fallo real: `oficina tarea fallar T-0042 --motivo "<una línea>"` (3 fallos
  seguidos pausan tu departamento — breaker; no lo esquives).
- Los entregables van a archivos en `~/office/departments/<dept>/` o a PRs del
  repo de gobierno; el tablero guarda referencias, no contenidos largos.

## 2. Política de marcas (la regla que no se negocia)

**ANTES de cualquier acción externa** (publicar, desplegar público, contactar
a un tercero, gastar, tocar un proyecto existente) consulta:

```
oficina politica check --accion-externa publish --marca <slug> [--importe N]
```

- exit 0 (ALLOW) → adelante; registra el evento y sigue el checklist de compliance.
- exit 3 (GATE) → abre gate y **espera** (silencio = pendiente, jamás timeout):
  `oficina gate abrir --tarea T-0042 --riesgo R2 --tipo publish --que "<1 línea>" --porque "<1 línea + enlaces>" --rollback "<≤2 líneas>"`
- exit 4 (DENY) → no existe ruta. No lo intentes por otra vía; si crees que
  merece excepción, entrégalo como propuesta interna en el resultado.

Traducción práctica: **marcas protegidas (ezti, musica, hotel, hermes-core…)
= como mucho propuesta/borrador/staging + gate. Marcas de oficina (creadas por
la oficina) = puedes ejecutar y publicar, con compliance y registro. Terceros
reales = gate R3 siempre. Marca sin registrar = protegida (fail-closed).**

## 3. Compliance en publicaciones autónomas (marcas de oficina)

Antes de publicar bajo marca de oficina, verifica y deja constancia en el
resultado: (a) claims legales (alimentación → skill `ezti-claims` como
plantilla del checklist 1924/2006); (b) RGPD si hay captura de datos;
(c) idioma revisado (ES/EU/EN según destino); (d) coste dentro de límite.
Después: `oficina evento log --tipo publicacion --mensaje "<qué y dónde>" --ref T-0042`.

## 4. Higiene

- Una nota del propietario en la tarea (`notas[]`) es una orden: intégrala.
- Escribe en español, con fuentes primarias + fecha + confianza donde aplique.
- No dupliques: antes de crear una tarea, `oficina tarea lista` y busca.
- Lo institucional (hechos verificados, decisiones, specs) va al repo vía PR
  (doc 09 §3); tu memoria de Hermes no sustituye al archivo.
