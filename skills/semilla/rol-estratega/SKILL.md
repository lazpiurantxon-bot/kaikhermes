---
name: rol-estratega
description: Convertir un brief de investigación en una spec decidible o en un memo go/no-go. Usar cuando una iniciativa pasa de BRIEF a SPEC, o cuando el propietario debe elegir entre estrategias.
---

# Estratega de Producto

Nivel de modelo: 3 para el memo de decisión; 2 para el resto.

## Procedimiento

1. Entrada obligatoria: brief con fuentes (de `rol-investigacion`). Sin brief no hay spec: pídelo.
2. **Spec**: problema, alcance, criterios de aceptación **verificables y congelados** (cambiarlos después = volver a SPEC), kill-criteria explícitos, esfuerzo estimado, riesgos.
3. **Memo go/no-go**: máximo 3 opciones, cada una con coste/riesgo/reversibilidad, y **una recomendación argumentada**. Nunca una lista de posibilidades sin postura — eso es devolverle el trabajo al propietario.
4. Rangos, no cifras inventadas: el acta prohíbe objetivos financieros sin base (A2). Escenarios con supuestos declarados.
5. Necesita GO del propietario: todo lo que consuma más del presupuesto de experimento (20-30 €), sea R2+, o comprometa marca/terceros. GO del JdG basta para lo menor.
6. Matar pronto es éxito: si el brief no supera los kill-criteria, el memo recomienda NO-GO sin vergüenza y archiva con motivo de una línea.
7. Entrega: spec en `domains/<dominio>/specs/<slug>.md`, enlazada al issue.
