"""Motor de política de marcas y acciones externas (determinista, fail-closed).

Es la barrera intermedia del doc 09 §4: la primera es material (las
credenciales de las marcas protegidas NO se instalan en la VM), la tercera son
los prompts/skills. Aquí no decide ningún LLM: la política es una tabla que
aplican por igual el CLI `oficina` (agentes) y el panel (propietario).

Regla central (ADR-004 / enmienda E1 del acta):
- Marcas PROTEGIDAS (EZTI, música, hotel, el propio sistema…): la oficina
  jamás publica, despliega ni modifica nada en su nombre por sí sola.
  Todo termina en GATE (propuesta que decide el propietario) o DENY (prohibido).
- Marcas de OFICINA (creadas por la propia oficina): publicación y operación
  autónomas (R1), con checklist de compliance embebido y registro visible.
- Contacto directo con terceros reales: SIEMPRE gate R3, sea cual sea la marca.
- Marca desconocida o sin declarar: se trata como protegida (fail-closed).
"""
from __future__ import annotations

from dataclasses import dataclass

ACTIONS = [
    "internal",          # investigar, redactar, código en branch, docs internos
    "create_brand",      # registrar una marca nueva de la oficina
    "publish",           # contenido público (web, redes, notas) bajo una marca
    "deploy_public",     # desplegar servicio/URL pública bajo una marca
    "contact",           # mensaje/email a un tercero real
    "spend",             # gasto en € reales
    "modify_protected",  # tocar activos/repos/infra de un proyecto existente
]

RISK_ORDER = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}


@dataclass
class Verdict:
    decision: str  # allow | gate | deny
    risk: str      # R0-R3
    reason: str

    @property
    def allowed(self) -> bool:
        return self.decision == "allow"

    def as_dict(self) -> dict:
        return {"decision": self.decision, "risk": self.risk, "reason": self.reason}


def evaluate(action: str, brand: dict | None, amount_eur: float | None = None,
             per_task_limit_eur: float = 20.0, spend_freeze: bool = False) -> Verdict:
    """Evalúa una acción. `brand` es la entrada del registro de marcas o None."""
    if action not in ACTIONS:
        return Verdict("deny", "R3", f"Acción desconocida '{action}': no existe ruta (fail-closed).")

    if action == "internal":
        return Verdict("allow", "R0", "Trabajo interno reversible: autónomo, queda en el log.")

    if action == "create_brand":
        return Verdict(
            "allow", "R1",
            "Crear marca de oficina: autónomo (enmienda E1). Queda registrada, "
            "aparece en el resumen diario y su primer uso público se notifica.",
        )

    if action == "contact":
        if brand and brand.get("enforcement") == "deny":
            return Verdict("deny", "R3",
                           f"Contacto bajo '{brand['slug']}': prohibido ({brand.get('notas', '')}).")
        return Verdict("gate", "R3",
                       "Contacto con terceros reales: gate R3 siempre; el envío final lo hace "
                       "o aprueba el propietario (acta B/E, sin cambios en la enmienda E1).")

    if action == "spend":
        if amount_eur is None:
            return Verdict("gate", "R3", "Gasto sin importe declarado: gate (fail-closed).")
        if spend_freeze:
            return Verdict("gate", "R3",
                           "Circuit breaker de presupuesto activo (>80% del techo mensual): "
                           "todo gasto nuevo requiere gate.")
        if amount_eur <= per_task_limit_eur:
            return Verdict("allow", "R1",
                           f"Gasto {amount_eur:.2f} € ≤ límite por tarea "
                           f"({per_task_limit_eur:.2f} €): autónomo, se registra en el ledger.")
        return Verdict("gate", "R3",
                       f"Gasto {amount_eur:.2f} € supera el límite por tarea: gate R3.")

    # publish / deploy_public / modify_protected — dependen de la marca
    if brand is None:
        return Verdict("gate", "R2",
                       "Marca no declarada o no registrada: se trata como protegida "
                       "(fail-closed). Registra antes la marca de oficina o abre gate.")

    if brand.get("status") == "office":
        if action == "modify_protected":
            return Verdict("allow", "R1",
                           f"'{brand['slug']}' es marca de oficina: sus activos son de la oficina.")
        return Verdict("allow", "R1",
                       f"Publicación bajo marca de oficina '{brand['slug']}': autónoma (enmienda E1). "
                       "Obligatorio: checklist de compliance (claims, RGPD, idioma) antes de publicar; "
                       "queda en el feed y en el resumen diario para veto retroactivo.")

    # protected / retired / cualquier otro estado → nunca autónomo
    if brand.get("enforcement") == "deny":
        return Verdict("deny", "R3",
                       f"'{brand['slug']}' está en lista de prohibidos: "
                       f"{brand.get('notas', 'sin ruta')}. No existe gate para esto; "
                       "si procede, entrégalo como propuesta interna al propietario.")

    risk = "R3" if action == "modify_protected" else "R2"
    return Verdict("gate", risk,
                   f"'{brand['slug']}' es marca/proyecto protegido: la oficina prepara la propuesta "
                   "en borrador/staging y el propietario decide con APRUEBO/RECHAZO. "
                   "Nada se publica ni se toca en su nombre de forma autónoma.")
