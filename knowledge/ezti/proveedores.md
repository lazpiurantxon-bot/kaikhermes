# EZTI — Copackers y fabricantes candidatos

- **Elaborado:** 2026-07-06 · **Versión:** v0.1 (Sprint 1, primer barrido)
- **valido_hasta:** 2026-10-06 (datos de empresas: revalidar antes de decidir)
- **Estado global:** candidatos identificados, **ninguno contactado** (contactar = R3, requiere gate)
- **Método:** búsqueda web 2026-07-06; cada entrada con fuente. Confianza `media` = la empresa declara el servicio en su web; falta verificar MOQ/costes/certificaciones reales (eso se obtiene con el contacto).

## Criterios de cualificación (para el scoring tras las respuestas)

1. **Capacidad técnica:** llenado de gel viscoso base miel en sachet/monodosis (30–60 g) o stick; ideal doypack con tapón como opción futura.
2. **MOQ** compatible con primer lote comercial pequeño (objetivo: ≤10–20k unidades; a confirmar contra coste).
3. **Coste unitario** por tramos de volumen.
4. **Certificaciones:** registro sanitario propio, IFS/BRC o equivalente; opción ecológico si algún día interesa.
5. **Flexibilidad de receta:** aceptar fórmula propia natural (miel, limón, sal) sin obligar a su formulación estándar.
6. **Servicios:** pruebas de estabilidad/vida útil, apoyo de etiquetado, muestras previas.
7. **Logística e idioma:** España > UE > UK (el Brexit añade fricción de importación para vender en España/UE).

## Candidatos — España (prioridad alta)

| Empresa | Tipo | Por qué candidato | Fuente | Confianza |
|---|---|---|---|---|
| Sport Foods Labs | Laboratorio fabricación a terceros de nutrición deportiva | Declara fabricación a terceros/marca blanca incluyendo **geles** | https://sportfoodlab.com/ | media |
| Fabricantes de Suplementos | Laboratorio a terceros complementos/deportiva | Fabricación a terceros y marca blanca de nutrición deportiva | https://fabricantesdesuplementos.com/ | media |
| Barosa Labs | Fabricante de suplementos a medida | Suplementos a medida para terceros, líneas deportivas | https://barosalabs.com/ | media |
| Fabricantes de Complementos | Laboratorio a terceros dietética/deportiva | Formula, desarrolla y fabrica nutrición deportiva a terceros | https://fabricantesdecomplementos.com/ | media |
| Allpack-Stick | Envasador a terceros monodosis/stick alimentario | Envasado a terceros en stick/sachet para alimentación y dietéticos, sala blanca | http://www.allpackstick.es/envase-de-monodosis | media |
| Monopacker | Envasador a terceros monodosis | Líneas automatizadas para líquidos, **gel**, salsas y cremas | https://www.monopacker.com/envasados-monodosis | media |
| Sucrepack | Envasador monodosis desde 1970 | Especialista monodosis alimentario (histórico en azúcar/miel) | https://sucrepack.es/ | media |
| Envasados a Terceros | Envasador a terceros alimentario | Monodosis y mini-doypack para alimentación; cita expresamente miel entre los productos | https://www.envasados.es/mini-doypack-un-nuevo-formato-de-envase/ | media |
| Arna Apícola | Apícola con línea de monodosis de miel | Produce sobres monodosis de miel (13 g); **preguntar si hace maquila** para terceros | https://arnaapicola.es/producto/sobre-miel-en-monodosis-miel-13-gr/ | baja (maquila no confirmada) |

Nota: los "laboratorios de suplementos" y los "envasadores alimentarios" son dos vías distintas — un gel de miel/limón/sal puede tratarse como **alimento** (no necesariamente como complemento alimenticio), lo que abre la vía del envasador alimentario clásico, a menudo con costes menores. Ver `normativa-alimentaria.md` §0 (clasificación) — decisión con flag de asesor.

## Candidatos — resto de Europa

| Empresa | País | Por qué candidato | Fuente | Confianza |
|---|---|---|---|---|
| Pouch Alliance | Países Bajos | Especialista en **geles energéticos** y líquidos para marcas privadas; sachets monodosis y doypacks 15–1000 ml | https://pouchalliance.com/ | media-alta (especialización exacta) |
| MillMax | UE (este) | Fabricación a terceros de deportiva incl. geles y líquidos, normas UE | https://millmax.eu/sport/ | media |
| Calleva Nutrition | Reino Unido | Productor histórico de geles deportivos en sachet, millones de unidades/año | https://www.calleva-nutrition.com/ | media — **fricción Brexit** |
| Vitrition | Reino Unido | Geles en sachets sellados individuales | https://www.vituk.com/gels/ | media — **fricción Brexit** |
| Unette | Reino Unido | Marca blanca de deportiva en sachet | https://www.unette.co.uk/white-label-solutions/sports-nutrition/ | media — **fricción Brexit** |

## Priorización para primer contacto (v0.2, 2026-07-06)

Propuesta de 6 para la primera oleada — mezcla deliberada de las dos vías (especialista en gel deportivo vs envasador alimentario) para comparar costes y MOQ reales:

| # | Empresa | Vía | Motivo de prioridad |
|---|---|---|---|
| 1 | Pouch Alliance (NL) | Especialista gel | Especialización exacta en geles energéticos de marca privada; referencia de mercado para calibrar al resto |
| 2 | Sport Foods Labs (ES) | Lab deportivo | Geles a terceros declarados, en España |
| 3 | Monopacker (ES) | Envasador | Declara llenado de **gel** en monodosis automatizada |
| 4 | Allpack-Stick (ES) | Envasador | Stick/sachet alimentario en sala blanca |
| 5 | Envasados a Terceros (ES) | Envasador | Monodosis/mini-doypack alimentario, cita miel |
| 6 | MillMax (UE) | Lab deportivo | Contraste de precio fuera de España, normas UE |

Reserva (2ª oleada si la 1ª no cuaja): Barosa Labs, Fabricantes de Suplementos, Fabricantes de Complementos, Sucrepack, Arna Apícola (maquila por confirmar). UK (Calleva, Vitrition, Unette): solo si las vías UE fallan, por fricción Brexit.

**Pendiente antes del envío:** verificar ficha y email de contacto de cada priorizado, y personalizar el borrador por empresa. El envío en sí = gate R3 individual del propietario, que además lo ejecuta él (el sistema no tiene capacidad de envío por diseño).

## Huecos declarados

- Ningún dato real de MOQ/costes todavía (se obtiene contactando, no está publicado).
- Emails de contacto de los 6 priorizados sin verificar todavía.
- Maquila de Arna Apícola no confirmada.
- No verificado si alguno acepta volúmenes de arranque muy pequeños (test de mercado <5k uds).
