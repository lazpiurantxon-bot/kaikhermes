# agency-agents: hechos de integración con Hermes + biblioteca de especialistas — v1

- **Fecha:** 2026-07-07 · **Fuente:** repo público [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT), commit `71394d83e9b5f73ef6e3f044fdc97e95a68f0e59`, leído en sesión (código de instalación + plugin generado, con CI propio).
- **valido_hasta:** 2027-01-07 (revalidar contra la versión de Hermes instalada; los hechos §1 se confirman en B7/B12 y se anotan en el issue #5).
- **Confianza:** media — es código de terceros que funciona contra Hermes real, no documentación oficial de Nous Research. Sirve para desatascar los [TBV] de `office/hermes/instalacion.md` con candidatos concretos, no para darlos por cerrados.
- **Decisión asociada:** `decisions/ADR-005` (adopción selectiva; prohibido importar el roster al catálogo de skills).

## 1. Hechos sobre Hermes Agent observados en su código de integración

Extraídos de `scripts/install.sh`, `scripts/build-hermes-plugin.py` e
`integrations/hermes/README.md` de ese repo:

| Hecho | Detalle | Confianza |
|---|---|---|
| Home del daemon | `${HERMES_HOME:-~/.hermes}` | alta (convención usada por su instalador y detector) |
| Config | `~/.hermes/config.yaml` | alta |
| Plugins | directorio `~/.hermes/plugins/<nombre>/`; se activan añadiendo el nombre a la lista `plugins.enabled:` de `config.yaml`; requiere reiniciar sesiones/gateway para redescubrir el toolset | media-alta |
| Formato de plugin | directorio con `plugin.yaml` (`name`, `version`, `description`, `provides_tools:`) + `__init__.py` en Python que define los tools (descripción + JSON Schema) | media-alta |
| Skills externas | clave de config `skills.external_dirs:` — lista de directorios que Hermes escanea y **anuncia en el catálogo inicial** de skills | media (citada repetidamente como mecanismo real; confirmar clave exacta en la versión instalada) |
| Delegación | existe un tool nativo `delegate_task` (su router lo usa "when available") — encaja con los subagentes aislados de ADR-004 | media |
| Coste de catálogo | cargar cientos de skills por `external_dirs` infla el catálogo inicial del daemon; por eso ellos usan un plugin router lazy. Con nuestras 19 skills no aplica | alta (razonamiento, no dato) |

## 2. Qué es agency-agents

~280 definiciones de especialistas en markdown con frontmatter
(`name`/`description`/`color` + identidad, misión, reglas críticas,
entregables, métricas), organizadas en 21 divisiones, con instaladores para
las principales herramientas agénticas. Para Hermes generan el plugin
**`agency-agents-router`**: 4 tools (`agency_agents_search`, `_inspect`,
`_load`, `_delegate`) que buscan y cargan especialistas bajo demanda desde
un JSON en disco, sin tocar el catálogo de skills.

Instalación (opcional, post-B12): `office/hermes/instalacion.md` §6.

## 3. Mapa de divisiones útiles por departamento (si el router está instalado)

| Departamento | Divisiones/especialistas relevantes |
|---|---|
| `dep-mercado` | `sales/` (pipeline-analyst, account-strategist), `finance/` (investment-researcher, fpa-analyst), `specialized/specialized-pricing-analyst`, `academic/` (geographer, anthropologist para contexto de mercado) |
| `dep-producto` | `product/`, `engineering/`, `testing/` (reality-checker, evidence-collector), `project-management/` |
| `dep-marketing` | `marketing/` (36 especialistas: growth, contenido, social, AEO/SEO), `paid-media/`, `support/analytics-reporter` |
| `dep-marca` | `design/` (brand-guardian, visual-storyteller, ui/ux, image-prompt-engineer), naming y posicionamiento en `marketing/` |

## 4. Límites de uso (gobernanza)

- Los especialistas son **contexto puntual por tarea** (search → load), no
  skills: el catálogo cerrado del PLAN §3 no cambia.
- Son prompts genéricos en inglés: método/checklist prestado, nunca
  sustituyen el procedimiento propio (fuente primaria, política de marcas,
  `oficina politica check`, gates R2/R3 — todo sigue mandando).
- Prohibido `skills.external_dirs` apuntando al roster y prohibido copiar
  agentes a `skills/` fuera del ciclo gobernado (retro → proposed → QA →
  merge humano).
