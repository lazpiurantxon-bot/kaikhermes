# 03 — Memoria, skills y knowledge base

## 1. Principio: memoria = git; nada aprende en silencio

Toda memoria persistente del sistema es **texto versionado en el repo de gobierno**, escrito por humanos o propuesto por agentes vía PR. No hay memoria opaca (embeddings, stores propietarios, "el agente recuerda") en F0–F2. Razones: auditabilidad total (diff de cada cambio de memoria), rollback trivial, cero coste, y elimina por construcción el autoaprendizaje peligroso — un agente no puede cambiar su propio comportamiento sin dejar un PR que alguien revisa.

## 2. Clases de memoria

| Clase | Dónde | Qué contiene | Qué NO contiene | Escritura |
|---|---|---|---|---|
| **Conocimiento** | `knowledge/<dominio>/` | Hechos durables verificados: dossiers (copackers, normativa, mercado), datos de producto, contactos de proveedores | Opiniones sin fuente, datos sin fecha, especulación | Agente propone PR → merge según nivel (§4) |
| **Decisiones** | `decisions/ADR-NNN.md` | Decisiones con contexto, opciones consideradas y consecuencias. Append-only | Nada se edita ni borra: se supersede | JdG redacta; decisiones R2+ las apruebas tú |
| **Playbooks** | `playbooks/`, `domains/*/playbook.md` | Cómo se hace cada rol/dominio: límites, tono, pasos, gates | Secretos, datos personales | PR con revisión humana siempre |
| **Skills** | `skills/proposed/` → `skills/approved/` | Procedimientos reutilizables promovidos desde experiencia real | Skills con acciones externas sin gate embebido | Ciclo de promoción (§3) |
| **Memoria de trabajo** | `work/<iniciativa>/` en el branch de la iniciativa | Notas, borradores, resultados intermedios | — | Libre; **se destila o se borra al cerrar** la iniciativa |
| **Registro operativo** | `state/` en la VM (SQLite) | Ledger de gasto, log de acciones, healthchecks | Contenido de trabajo | Automática, determinista |

**Qué va a memoria persistente y qué no:** persiste lo que un agente futuro necesitará y no podrá rederivar barato (hechos verificados, decisiones, procedimientos probados). No persiste: transcripciones de sesiones, razonamiento intermedio, borradores muertos, resultados de experimentos fallidos (se registra la *conclusión* del fallo en una ADR o retro, no el cadáver completo).

## 3. Ciclo de vida de una skill

1. **Detección:** un patrón se repite ≥2 veces en trabajo real (p. ej. "publicar en Cloudflare Pages con checklist de claims").
2. **Borrador:** el agente (normalmente en la retro semanal) escribe `skills/proposed/<nombre>.md`: cuándo aplica, pasos, herramientas, gates de riesgo embebidos, criterios de éxito, contraindicaciones.
3. **Prueba:** la skill propuesta se usa en ≥2 encargos reales citando su versión; los resultados se anotan en el propio PR.
4. **Promoción:** revisión QA + **merge humano obligatorio** → `skills/approved/`. Ninguna skill se autopromociona.
5. **Revisión periódica:** cada skill lleva `revisar_antes_de:` (fecha). Las caducadas vuelven a `proposed/` o se archivan.

Regla dura: cualquier skill que implique acción externa (publicar, contactar, gastar, desplegar a prod) lleva su gate R2/R3 **dentro del procedimiento**, de modo que ni siquiera un agente que cargue la skill "por error" pueda saltarse la aprobación.

## 4. Gobernanza de escritura: quién puede mergear qué

| Cambio | Aprobación necesaria |
|---|---|
| `work/` (memoria de trabajo) | Ninguna (vive y muere con el branch) |
| `knowledge/` — hechos con fuente primaria citada | QA-agente puede aprobar; muestreo humano semanal |
| `knowledge/` — datos legales, fiscales, de contratos | Humano siempre, con marca "pendiente de verificación profesional" cuando aplique |
| `playbooks/`, `skills/approved/`, límites de riesgo | **Humano siempre** |
| `decisions/` (ADRs) | Humano para decisiones R2+; JdG para R0/R1 (quedan en el resumen diario) |

## 5. Anti-basura y anti-deriva

- **Todo hecho lleva fuente + fecha + confianza** (`alta/media/baja`). Lo que no las tiene no entra en `knowledge/`.
- **Destilar > acumular:** al cerrar una iniciativa, el Documentalista extrae lo durable (media página bien escrita vale más que 20 páginas de notas) y el resto muere con el branch.
- **TTL en hechos volátiles:** precios, MOQs, plazos de ayudas y datos de mercado llevan fecha de caducidad; el watchdog lista mensualmente lo caducado y el JdG decide refrescar o archivar.
- **Presupuesto de tamaño:** si `knowledge/` de un dominio supera ~50 documentos, la retro debe consolidar antes de añadir más. El síntoma de memoria basura es crecimiento sin consulta: el Documentalista registra qué documentos se citan en encargos; lo que nadie cita en 2 meses es candidato a archivo.
- **Sin reglas de comportamiento autoaprendidas:** un agente puede *proponer* "deberíamos hacer siempre X", jamás aplicarlo sin merge humano en playbook o skill.

## 6. Estructura de la knowledge base

```
knowledge/
├── INDEX.md                  # todo a ≤2 saltos de aquí
├── ezti/
│   ├── producto.md           # receta, formatos, claims permitidos
│   ├── proveedores.md        # copackers: MOQ, costes, estado de contacto
│   ├── normativa-alimentaria.md  # 1169/2011, 1924/2006, RGSEAA (+flags de verificación)
│   ├── fiscal-facturacion.md # TicketBAI/facturación — módulo de operación comercial, posterior
│   ├── mercado.md            # competidores, precios, posicionamiento
│   └── ayudas.md             # subvenciones con plazos (TTL corto)
├── core/                     # decisiones técnicas del propio sistema
├── musica/                   # catálogo, opciones de distribución (privado)
└── hotel/                    # SOLO material genérico; prohibido dato de huésped
decisions/ADR-001.md …        # append-only
```

El tablero (GitHub Issues) referencia documentos por ruta; los documentos referencian issues por número. Esa doble referencia es lo que te permite auditar cualquier decisión meses después sin arqueología.
