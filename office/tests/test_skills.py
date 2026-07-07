"""Lint estructural del catálogo canónico de skills (skills/**/SKILL.md).

Hace determinista lo que hasta ahora solo vigilaba la retro semanal leyendo:

- formato agentskills.io mínimo que Hermes consume (frontmatter con name y
  description; name == nombre del directorio);
- la regla dura de skills/README.md: **toda skill con acción externa
  (publicar, contactar, gastar, desplegar) lleva su gate embebido** en el
  procedimiento;
- clasificación fail-closed: una skill nueva que no esté clasificada aquí
  rompe la suite — quien la añada (humano o retro) debe declarar si tiene
  acción externa, en el mismo PR.

Adoptado de la idea del CI de agency-agents (ADR-005); implementación propia
en stdlib, como el resto de office/.
"""
import re
from pathlib import Path

import pytest

REPO_DIR = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_DIR / "skills"

# Clasificación canónica (fail-closed): skill fuera de estas listas = error.
# "Acción externa" según skills/README.md: publicar, contactar, gastar,
# desplegar a prod — o custodiar el propio gate.
CON_ACCION_EXTERNA = frozenset({
    "jdg-gate",              # es el gate
    "outreach-r3",           # contacto con terceros
    "ezti-claims",           # bloquea publicación
    "rol-sre",               # deploy a prod
    "orquestador-despacho",  # despacha gates y habla con el propietario
    "oficina-protocolo",     # protocolo común: embebe la política de marcas
    "dep-mercado",           # riesgo de contacto; suscripciones = spend
    "dep-producto",          # puede desplegar/publicar bajo marcas de oficina
    "dep-marketing",         # publica bajo marcas de oficina
    "dep-marca",             # crea/publica marcas de oficina
})
SIN_ACCION_EXTERNA = frozenset({
    "jdg-triaje",
    "jdg-resumen-diario",
    "rol-investigacion",
    "rol-estratega",
    "rol-constructor",
    "rol-qa",
    "rol-documentalista",
    "retro-semanal",
    "ledger",
})

GATE_RE = re.compile(r"gate|pol[ií]tica", re.IGNORECASE)

SKILL_FILES = sorted(SKILLS_DIR.rglob("SKILL.md"))
IDS = [p.parent.name for p in SKILL_FILES]


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None, text
    fields = {}
    for line in parts[1].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, parts[2]


def test_hay_skills():
    assert len(SKILL_FILES) >= 19, "el catálogo canónico (13 semilla + 6 oficina) no está completo"


def test_clasificacion_cubre_el_catalogo():
    en_repo = {p.parent.name for p in SKILL_FILES}
    solapadas = CON_ACCION_EXTERNA & SIN_ACCION_EXTERNA
    assert not solapadas, f"skills en ambas listas: {sorted(solapadas)}"
    sin_clasificar = en_repo - CON_ACCION_EXTERNA - SIN_ACCION_EXTERNA
    assert not sin_clasificar, (
        f"skills sin clasificar: {sorted(sin_clasificar)} — decide si tienen acción "
        "externa y añádelas a CON_ACCION_EXTERNA o SIN_ACCION_EXTERNA en este test "
        "(regla dura de skills/README.md)"
    )
    fantasma = (CON_ACCION_EXTERNA | SIN_ACCION_EXTERNA) - en_repo
    assert not fantasma, f"clasificadas pero sin SKILL.md en el repo: {sorted(fantasma)}"


@pytest.mark.parametrize("path", SKILL_FILES, ids=IDS)
def test_formato_agentskills(path):
    text = path.read_text(encoding="utf-8")
    assert "\r" not in text, f"{path}: finales de línea CRLF; el repo usa LF"
    fields, body = parse_frontmatter(text)
    assert fields is not None, f"{path}: falta frontmatter YAML delimitado por ---"
    name = fields.get("name", "")
    assert name, f"{path}: frontmatter sin 'name'"
    assert name == path.parent.name, (
        f"{path}: name '{name}' != directorio '{path.parent.name}'"
    )
    description = fields.get("description", "")
    assert description, f"{path}: frontmatter sin 'description'"
    assert len(description) <= 1024, f"{path}: description supera 1024 caracteres"
    cuerpo_util = [l for l in body.splitlines() if l.strip()]
    assert len(cuerpo_util) >= 5, f"{path}: cuerpo casi vacío ({len(cuerpo_util)} líneas)"


@pytest.mark.parametrize(
    "path",
    [p for p in SKILL_FILES if p.parent.name in CON_ACCION_EXTERNA],
    ids=[p.parent.name for p in SKILL_FILES if p.parent.name in CON_ACCION_EXTERNA],
)
def test_accion_externa_lleva_gate_embebido(path):
    _, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    assert GATE_RE.search(body), (
        f"{path}: skill con acción externa sin mención a su gate/política en el "
        "procedimiento — viola la regla dura de skills/README.md"
    )
