# Skills de la oficina autónoma (ADR-004)

Catálogo de la **oficina de departamentos** sobre Hermes Agent. Se instalan en
el daemon junto a las 13 skills semilla (`skills/semilla/`), que siguen
vigentes: los departamentos *usan* los roles semilla (investigación,
estratega, constructor, QA, documentalista) como procedimientos internos.

| Skill | Quién la carga | Cuándo |
|---|---|---|
| `oficina-protocolo` | todos | siempre (referenciada por las demás) |
| `orquestador-despacho` | agente raíz (JdG) | cron cada 15 min + al recibir mensaje del propietario |
| `dep-mercado` | subagente aislado | pulso proactivo diario + encargos |
| `dep-producto` | subagente aislado | pulso proactivo 2×/día + encargos |
| `dep-marketing` | subagente aislado | pulso proactivo diario + encargos |
| `dep-marca` | subagente aislado | pulso proactivo cada 2 días + encargos |

**Reglas (heredadas de `skills/semilla/README.md`, sin cambios):**
1. La versión de este repo es la canónica; la retro semanal reconcilia parches.
2. Toda skill con acción externa lleva su gate embebido — aquí además el
   veredicto lo da `oficina politica check` (determinista, fail-closed).
3. Los departamentos asumen cargado el playbook del dominio afectado y el acta
   (`operating-model/fase-1-respuestas.md`, incluida la **enmienda E1**).

**La frontera de marcas, en una línea:** marca protegida → como mucho
*propuesta + gate*; marca de oficina → ejecución autónoma con compliance;
terceros reales → gate R3 siempre; duda → fail-closed.
