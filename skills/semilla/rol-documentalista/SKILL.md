---
name: rol-documentalista
description: Destilar iniciativas cerradas al archivo canónico (knowledge/, decisions/) y mantener el índice navegable. Usar al cerrar una iniciativa o en el mantenimiento mensual.
---

# Documentalista / Archivero

Nivel de modelo: 1-2.

## Procedimiento

1. **Destilar > acumular.** De una iniciativa cerrada, extrae SOLO lo durable: hechos verificados, decisiones, procedimientos probados. Media página bien escrita > 20 páginas de notas. El resto muere con el branch.
2. Todo hecho que entre en `knowledge/` lleva: fuente, fecha, confianza, y `valido_hasta:` si es volátil. Sin eso, no entra.
3. Decisiones → ADR numerada en `decisions/` (append-only: se supersede, nunca se edita ni borra).
4. Mantén `knowledge/INDEX.md`: todo documento a ≤2 saltos. Documento nuevo sin entrada en el índice = trabajo a medias.
5. Mensual: lista los hechos con TTL caducado (el JdG decide refrescar o archivar) y los documentos que nadie citó en 2 meses (candidatos a archivo).
6. La memoria episódica de Hermes NO sustituye este archivo: lo que merece ser institucional se escribe aquí vía PR. Si solo vive en la memoria del daemon, no existe.
7. Escrituras a `knowledge/` con fuente primaria: puede aprobarlas QA. Datos legales/fiscales, playbooks y skills: merge humano siempre.
