# EZTI — Compliance alimentario de producto (v1)

- **Elaborado:** 2026-07-06 por el sistema. **NO es asesoramiento legal.** Cada sección lleva flag de verificación profesional; nada de este documento se presenta ni se firma sin revisión humana (acta E14).
- **Alcance:** normativa de PRODUCTO. Facturación/fiscalidad (TicketBAI) es un módulo separado y posterior (`fiscal-facturacion.md`, ADR-002).
- Confianza global: **media-alta** en la identificación de las normas aplicables; **las condiciones de detalle exigen asesor alimentario** antes del primer lote con copacker.

## 0. Clasificación del producto ⚑ CRÍTICO — verificar con asesor

Un gel de miel, limón y sal es, en principio, un **alimento** (preparación alimenticia), no automáticamente un "complemento alimenticio" (regulados por el RD 1487/2009). La clasificación condiciona etiquetado, registro y hasta qué copacker sirve. Decidir la clasificación con asesor **antes** de encargar etiquetas o lote.

## 1. Etiquetado — Reglamento (UE) 1169/2011

- Fuente primaria: https://eur-lex.europa.eu/eli/reg/2011/1169/oj (consultar versión consolidada)
- Menciones obligatorias (art. 9): denominación del alimento; lista de ingredientes; **alérgenos destacados** (la mostaza, el gluten o los sulfitos no aplican a priori a miel/limón/sal, pero revisar coadyuvantes del copacker); cantidad neta; fecha de duración mínima; condiciones de conservación; nombre y dirección del operador; país de origen cuando proceda; **información nutricional** (valor energético, grasas, saturadas, hidratos, azúcares, proteínas, sal).
- **Venta a distancia (art. 14):** toda la información obligatoria (salvo fecha de duración) debe estar disponible **antes de que se realice la compra** — es decir, en la ficha de producto de la web de EZTI.
- Idiomas: al menos castellano para venta en España.
- ⚑ Verificar: tamaño mínimo de letra, formato de la tabla nutricional y mención de origen de la miel (existe normativa específica de etiquetado de mezclas de mieles — Directiva de la miel y su transposición; relevante si la miel es ingrediente principal declarado).

## 2. Claims — Reglamento (CE) 1924/2006 ⚑ EL MAYOR RIESGO DE MARCA

- Fuente primaria: https://eur-lex.europa.eu/eli/reg/2006/1924/oj · Registro de declaraciones autorizadas de la UE: https://ec.europa.eu/food/food-feed-portal/screen/health-claims/eu-register
- Regla: **solo se pueden usar declaraciones nutricionales y de salud autorizadas**, con sus condiciones de uso exactas. Todo lo demás está prohibido, aunque sea "obviamente cierto".
- Implicaciones prácticas para EZTI:
  - "Energético" como descripción comercial requiere cuidado: las declaraciones sobre hidratos de carbono y sobre **soluciones de hidratos de carbono y electrolitos** existen en el registro con condiciones de composición específicas (p. ej. contenido de sodio y osmolalidad); un gel puede no cumplir las condiciones de "solución". ⚑ Verificar con asesor si la fórmula cumple las condiciones de alguna declaración autorizada antes de usarla.
  - Prohibido atribuir a la miel propiedades de prevención o curación de enfermedades (art. 7 del 1169/2011 y marco del 1924/2006).
  - Frases de marketing tipo "mejora el rendimiento", "recupera antes", "más resistencia" son claims de salud: **no usarlas sin respaldo del registro**.
- Mecanismo interno: checklist de claims obligatorio en QA antes de cualquier gate de publicación (playbook EZTI).

## 3. Registro sanitario — RGSEAA (RD 191/2011)

- Fuente primaria: https://www.boe.es/eli/es/rd/2011/02/18/191
- Las empresas alimentarias deben estar inscritas en el RGSEAA (o registro autonómico según actividad) **antes** de iniciar actividad; el trámite se gestiona vía la autoridad sanitaria autonómica (en Euskadi, Departamento de Salud del Gobierno Vasco).
- Situación EZTI: ya se vende producto → ⚑ **confirmar el estado de inscripción actual** (propia o amparada en el registro del elaborador). Si el copacker fabrica, su instalación debe tener RGSEAA con la actividad correspondiente, y EZTI como comercializadora/marca puede requerir su propia inscripción. Verificar ambas cosas con asesor: es barato y es lo primero que mira una inspección.

## 4. Venta online

- LSSI-CE (Ley 34/2002): identificación del vendedor, condiciones, proceso de compra. Fuente: https://www.boe.es/eli/es/l/2002/07/11/34
- Consumidores (TRLGDCU, RDL 1/2007): derecho de desistimiento y sus **excepciones** para bienes perecederos o precintados de higiene ⚑ verificar encaje exacto de un gel alimentario.
- 1169/2011 art. 14 (§1 de este doc): información obligatoria en la ficha antes de comprar.

## 5. Pruebas de estabilidad / vida útil

No hay un reglamento único: la fecha de duración mínima la fija el operador **con base justificable** (estudios de estabilidad, aw/pH — la miel es poco propensa pero el limón cambia pH y el formato sachet importa). Los copackers serios lo ofrecen como servicio: está en los criterios de cualificación de `proveedores.md`. ⚑ Exigir informe de estabilidad como entregable del copacker elegido.

## Checklist operativo (estado)

- [ ] Clasificación del producto decidida con asesor (§0)
- [ ] Estado RGSEAA de EZTI confirmado (§3)
- [ ] Etiqueta actual auditada contra art. 9 del 1169/2011 (§1)
- [ ] Ficha web auditada contra art. 14 (§1, §4)
- [ ] Lista de claims permitidos/prohibidos para EZTI redactada y aprobada (§2)
- [ ] Informe de estabilidad previsto en el contrato con copacker (§5)
