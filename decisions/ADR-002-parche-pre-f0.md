# ADR-002 — Parche correctivo pre-F0 (obligatorio, ordenado por el propietario)

- **Fecha:** 2026-07-06
- **Estado:** aceptada y aplicada
- **Nivel:** R1 (corrección de diseño antes de ejecutar infraestructura)

## Correcciones aplicadas

1. **Gmail (corrección de afirmación falsa).** `gmail.compose` NO hace al sistema técnicamente incapaz de enviar: según Google permite gestionar borradores **y enviar correo**. Política corregida: el agente solo recibe `gmail.readonly`; nunca `gmail.compose`, `gmail.modify` ni `gmail.send`. Los borradores se generan como Markdown/EML en repo o cola interna. Si en el futuro se quieren borradores reales en Gmail, será mediante un mediador mínimo sin endpoints de envío expuestos al agente, con tests de bloqueo, y documentado como control de software propio — no como garantía OAuth pura. (Docs 02, 04, 07, 08.)
2. **Clean-room matizado.** Se afirma: repo clean-room verificable por root commit, y proceso clean-room declarado. NO se afirma garantía absoluta sobre el conocimiento humano (o del modelo) previo. (Docs 00, 02, README.)
3. **TicketBAI separado del dossier alimentario.** 1169/2011, 1924/2006 y RGSEAA = compliance alimentario de producto. TicketBAI = facturación/fiscalidad, módulo posterior de operación comercial. (Docs 00, 03, 07.)
4. **Fable 5.** Se mantiene como recurso escaso (arquitectura, QA crítico, decisiones R2+). No se asume disponibilidad sostenida bajo el plan Pro; el ledger contabiliza cada uso de nivel 3. (Doc 04.)
5. **Precondiciones de VM.** Antes de tocar cualquier VM: snapshot creado **y probado**, inventario mínimo (metadatos, sin inspección de contenido), coste mensual estimado, rollback documentado, kill switch probado. Sin las cinco marcas no se ejecuta nada contra GCP. (Docs 02, 08.)

## Consecuencias

F0 queda autorizado tras el commit de este parche. Las cinco correcciones son vinculantes y cualquier reversión requiere nueva ADR aprobada por el propietario.
