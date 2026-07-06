# 07 — Aplicaciones personalizadas de alto apalancamiento

Cinco aplicaciones end-to-end sobre tus proyectos reales. Ninguna es un recordatorio bonito: todas producen activos, decisiones o despliegues.

---

## APP 1 — EZTI: Motor de Proveedores y Cumplimiento

*El desbloqueador del objetivo de 90 días: fabricante cerrado y primer lote comercial.*

- **Input inicial:** ficha de producto (receta miel/limón/sal, formato, volúmenes objetivo, coste unitario objetivo) que tú validas en 15 minutos.
- **Agentes:** JdG → Analista de Investigación (barrido de copackers ES/EU de geles/alimentación deportiva y miel), Estratega (modelo de scoring: MOQ, coste, certificaciones, plazos, flexibilidad de receta), Documentalista (dossier normativo), Revisor QA (verificación de fuentes y claims).
- **Herramientas:** búsqueda/lectura web, `knowledge/ezti/`, generación de hoja de costes, borradores Gmail (sin capacidad de envío).
- **Output final:** (1) shortlist rankeada de 8–15 copackers con MOQ/costes/certificaciones/contacto y estado; (2) dossier normativo: etiquetado Reglamento (UE) 1169/2011, claims nutricionales y de salud Reglamento (CE) 1924/2006 (crítico: qué NO puedes decir de un gel con miel), registro sanitario RGSEAA, TicketBAI para tu facturación en Gipuzkoa, requisitos de venta online — **cada punto con fuente primaria y flag "verificar con asesor/consultor alimentario"**; (3) modelo de coste unitario por escenario (copacker A/B/C × volumen) con rangos, no cifras inventadas; (4) borradores de email de contacto ES/EN por proveedor; (5) barrido de ayudas (SPRI, Diputación Foral de Gipuzkoa, líneas agroalimentarias) con plazos y requisitos.
- **Opera sola:** toda la investigación, scoring, dossier, modelo de costes y borradores (R0/R1).
- **Requiere tu revisión:** envío de cada email (R3), selección final de copacker, cualquier presentación de solicitud de ayuda (prohibida sin ti).
- **KPIs:** nº de copackers cualificados con datos completos; nº de respuestas obtenidas tras tus envíos; banda de coste unitario con confianza declarada; % checklist normativo completado; horas tuyas ahorradas (estimadas ≥30–40 h de investigación manual).
- **Riesgos:** datos regulatorios alucinados → mitigado con cita primaria obligatoria + flag profesional; datos de proveedores desactualizados → TTL en `knowledge/`; sesgo a proveedores con buena web → el brief exige incluir búsqueda vía asociaciones sectoriales.
- **Why-now / ROI:** es literalmente el camino crítico de tu objetivo a 90 días. Cada semana sin fabricante es una semana de estantería vacía y patrocinios sin producto que entregar.

---

## APP 2 — Hermes/Mandi: Pipeline "Idea → Prototipo desplegado"

*La meta-aplicación: el mecanismo honesto detrás de tu visión de 12 meses.*

- **Input inicial:** un mensaje de Telegram: `IDEA: <descripción>` (p. ej. el IoT de stock de bar, la app tipo TP-7, el agente CAM/CNC).
- **Agentes:** gateway (intake) → JdG (triage) → Analista (brief de validación: mercado, competidores, esfuerzo, kill-criteria) → Estratega (memo go/no-go, ≤3 opciones) → **[tu GO]** → Constructor (prototipo en repo propio, worktree aislado) → Revisor QA → Operador SRE (deploy interno).
- **Herramientas:** GitHub (repo nuevo por prototipo — autonomía (f)), Claude Code, VM/Docker o CF Pages preview, auth básica.
- **Output final:** por cada idea, o bien un **memo de kill con motivo** (resultado positivo: ideas muertas baratas), o bien un **prototipo funcional en URL interna** + spec + notas de "qué haría falta para producción" + estimación de coste/esfuerzo del siguiente paso.
- **Opera sola:** de idea a memo (siempre); de GO a prototipo interno desplegado (R0/R1 completo).
- **Requiere tu revisión:** el GO tras el memo; cualquier paso a dominio público, usuarios reales o compra (R2/R3).
- **KPIs:** lead time idea→memo ≤48 h; idea→prototipo interno ≤2 semanas (alcance pequeño); % de ideas matadas en BRIEF (sano: la mayoría); coste por experimento ≤ límite; nº de prototipos que promocionan a producto.
- **Riesgos:** dispersión de prototipos → WIP limit 2 + archivado automático de lo estancado >30 días; entusiasmo del Constructor sobre spec débil → el pipeline no permite BUILD sin criterios de aceptación congelados.
- **Why-now / ROI:** convierte tu lista de F18 (IoT bar, CAM/CNC, TP-7, Sísifo, 3D…) de "ideas en la cabeza" en una cola gobernada donde cada una muere barata o avanza con evidencia. Es la diferencia estructural entre tener ideas y tener un portafolio.
- **Nota sin suavizar:** la parte de tu visión "genera también contratos e implicaciones legales" sale de este pipeline como **borradores marcados para revisión profesional**, nunca como documentos válidos. Eso no es una limitación del diseño: es la única versión legal y segura de esa capacidad.

---

## APP 3 — EZTI: Fábrica de Presencia y Patrocinio

*Del producto que ya vendes a una máquina comercial con marca.*

- **Input inicial:** activos de marca actuales (logo, fotos, textos de la web actual), acceso Cloudflare scoped a `ezti.net`, lista de atletas/clubes locales candidatos.
- **Agentes:** Estratega (posicionamiento vs competidores de geles: naturales vs sintéticos, precio, narrativa local/vasca), Constructor (web nueva en CF Pages: ES/EU/EN, ficha de producto, historia, puntos de venta, captura de emails), Documentalista (checklist de claims 1924/2006 aplicado a cada texto), Analista (mapa de carreras/eventos y clubes de Gipuzkoa/Euskadi como canales), Revisor QA.
- **Herramientas:** Cloudflare Pages + DNS, repo `ezti-web`, analytics de Cloudflare, generación de PDFs (kit de patrocinio).
- **Output final:** (1) web nueva **en staging** lista para tu gate de publicación; (2) kit de patrocinio (one-pager PDF + condiciones tipo + hoja de seguimiento de atletas: quién, estado, coste en producto, alcance); (3) calendario editorial de 4–8 semanas con posts **en cola de borradores**; (4) mapa de eventos deportivos locales con fechas como plan comercial.
- **Opera sola:** todo hasta staging y borradores (R0/R1).
- **Requiere tu revisión:** publicar en `ezti.net` (R2), cada post público (R2), cada contacto con atleta/club (R3), condiciones de patrocinio (implican compromiso: R3).
- **KPIs:** web en staging con checklist de claims 100% pasado; N kits de patrocinio listos; tras tu publicación: conversión web base, emails capturados, patrocinios firmados por ti.
- **Riesgos:** claims de salud ilegales ("da energía", "mejora el rendimiento" tienen restricciones específicas) → checklist obligatorio con fuente por claim; euskera de calidad → el playbook exige revisión humana nativa antes de publicar EU.
- **Why-now / ROI:** ya tienes ventas web y quieres patrocinios este trimestre; cada mejora de conversión multiplica sobre tráfico existente, y los kits convierten "conozco a un atleta" en un proceso repetible.

---

## APP 4 — Música: Estudio de Catálogo y Preparación de Lanzamiento (privado)

*Estructura el dominio sin tocar ninguna línea roja de E13.*

- **Input inicial:** volcado desordenado de lo que exista: grabaciones, ideas, stems, vídeos de ensayos, notas — tú lo subes a un espacio privado, el sistema lo organiza.
- **Agentes:** Documentalista (inventario con metadatos: estado, calidad, potencial, qué falta), Estratega (propuesta de línea: EP vs singles vs contenido de batería; cadencia realista con tu tiempo), Analista (comparativa de distribuidoras y sus términos, opciones de alias, qué implica registrar marca — **solo información para decidir, sin ejecutar nada**), JdG (pipeline de producción con hitos).
- **Herramientas:** repo/almacenamiento privado, `knowledge/musica/`, búsqueda web.
- **Output final:** (1) catálogo 100% inventariado con estado por pieza; (2) memo de decisión: alias, tipo de producto musical, cadencia, con ≤3 opciones y recomendación; (3) dossier de distribución (términos, costes, derechos, exclusividades de las principales opciones) para que decidas con datos; (4) 1–2 piezas llevadas a estado "release-ready" en privado (checklist técnico: mezcla, master, metadatos, arte — encargos a humanos donde haga falta, presupuestados); (5) kit de directo: setlist, rider técnico tipo, mapa de salas locales con requisitos de contacto (contactar = R3, lo haces tú o apruebas cada mensaje).
- **Opera sola:** inventario, investigación, memos, checklists, organización (R0).
- **Requiere tu revisión:** toda decisión de identidad artística; cualquier publicación, registro, contacto o firma — **bloqueado** hasta que resuelvas los datos de E13, y aun entonces R3.
- **KPIs:** catálogo inventariado 100%; memo de decisión entregado; 1–2 piezas release-ready; dossier de distribución completo; primer directo agendado (por ti) con kit preparado.
- **Riesgos:** el principal es estratégico — invertir aquí tiempo de la oficina que EZTI necesita; mitigado: esta app corre a prioridad baja, sin deadline, consumiendo capacidad sobrante.
- **Why-now / ROI:** desbloquea tus propias preguntas abiertas (E13/F17). El sistema no puede publicar por ti, pero puede hacer que la decisión de estructurar tu música pase de "algún día" a un memo con opciones encima de tu mesa en dos semanas.

---

## APP 5 — Hotel: Generador de Propuestas Internas + Plan de Salida

*Sirve a tu objetivo real declarado — dejar el empleo — sin tocar ni un dato del empleador.*

- **Input inicial:** tus descripciones de procesos (sin datos reales de huéspedes ni credenciales): cómo es el check-in, qué reporting haces, dónde se pierde tiempo.
- **Agentes:** Analista (mejores prácticas de recepción, normativa aplicable tipo registro de viajeros/TicketBAI a nivel informativo), Estratega (propuestas internas con caso de negocio: ahorro de tiempo, errores evitados), Documentalista (formato presentable), y para el plan de salida: Estratega + Contralor.
- **Herramientas:** solo documentos; cero integración con sistemas del hotel (prohibido por diseño, no por promesa).
- **Output final:** (1) 2–3 propuestas de mejora presentables por ti a dirección (p. ej. rediseño del flujo de check-in, cartelería multilingüe ES/EU/EN/FR generada y lista para imprimir, checklists operativos de recepción/limpieza genéricos) — te posicionan profesionalmente mientras sigas allí; (2) **plan de salida cuantificado**: qué ingresos mensuales de EZTI+resto necesitas para dejar el hotel con N meses de colchón, actualizado mensualmente con datos que tú introduces, con hitos observables — el sistema no toca tu banca (Tier-0), tú le das los números.
- **Opera sola:** investigación, redacción, cartelería, actualización del plan con tus datos (R0).
- **Requiere tu revisión:** todo lo que entregues al hotel lo presentas tú como tuyo; el sistema no se comunica jamás con tu empleador.
- **KPIs:** propuestas entregadas y su acogida; horas/semana tuyas liberadas en tareas administrativas propias; runway del plan de salida con fecha estimada visible y su tendencia mes a mes.
- **Riesgos:** filtración accidental de datos del empleador al sistema → el playbook del dominio instruye rechazar y borrar cualquier dato de huésped o interno que aparezca; ambigüedad laboral → las propuestas son trabajo intelectual tuyo presentado por ti, el sistema es tu herramienta personal de redacción.
- **Why-now / ROI:** es la app más barata de las cinco y ataca la variable que declaraste central: tu tiempo y tu fecha de salida. El plan de salida convierte "quiero dejarlo" en una función de los KPIs de EZTI — une todos los dominios en un solo número que ves cada mes.
