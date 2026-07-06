# Skills

Ciclo de vida gobernado (doc `operating-model/03` §3):

- `proposed/` — borradores detectados por la retro (patrón repetido ≥2 veces). Deben probarse en ≥2 encargos reales citando versión.
- `approved/` — skills promovidas: revisión QA + **merge humano obligatorio**. Cada una con `revisar_antes_de:`.

Regla dura: toda skill con acción externa (publicar, contactar, gastar, desplegar a prod) lleva su gate R2/R3 embebido en el procedimiento.
