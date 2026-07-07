"""La política de marcas es la garantía central: se prueba como tabla."""
from core import policy


def brand(status, enforcement, slug="x"):
    return {"slug": slug, "status": status, "enforcement": enforcement, "notas": "n"}


def test_interno_siempre_permitido():
    v = policy.evaluate("internal", None)
    assert v.decision == "allow" and v.risk == "R0"


def test_marca_protegida_nunca_publica_sola():
    for action in ("publish", "deploy_public"):
        v = policy.evaluate(action, brand("protected", "gate", "ezti"))
        assert v.decision == "gate" and v.risk == "R2"


def test_modificar_proyecto_protegido_es_gate_r3():
    v = policy.evaluate("modify_protected", brand("protected", "gate", "ezti"))
    assert v.decision == "gate" and v.risk == "R3"


def test_marcas_prohibidas_no_tienen_ruta():
    for action in ("publish", "deploy_public", "contact", "modify_protected"):
        v = policy.evaluate(action, brand("protected", "deny", "hotel"))
        assert v.decision == "deny", action


def test_marca_de_oficina_publica_autonoma():
    v = policy.evaluate("publish", brand("office", "allow", "nueva"))
    assert v.decision == "allow" and v.risk == "R1"
    assert "compliance" in v.reason.lower()


def test_marca_desconocida_fail_closed():
    for action in ("publish", "deploy_public", "modify_protected"):
        assert policy.evaluate(action, None).decision == "gate", action


def test_contacto_terceros_siempre_gate():
    assert policy.evaluate("contact", None).decision == "gate"
    assert policy.evaluate("contact", brand("office", "allow")).decision == "gate"


def test_gasto():
    assert policy.evaluate("spend", None, amount_eur=10, per_task_limit_eur=20).decision == "allow"
    assert policy.evaluate("spend", None, amount_eur=50, per_task_limit_eur=20).decision == "gate"
    assert policy.evaluate("spend", None, amount_eur=None).decision == "gate"
    assert policy.evaluate("spend", None, amount_eur=1, spend_freeze=True).decision == "gate"


def test_crear_marca_permitido():
    assert policy.evaluate("create_brand", None).decision == "allow"


def test_accion_desconocida_deny():
    assert policy.evaluate("hackear", None).decision == "deny"


def test_seeds_reales(store):
    """Las marcas sembradas se comportan como promete la enmienda E1."""
    assert store.check_action("publish", marca="ezti").decision == "gate"
    assert store.check_action("publish", marca="musica").decision == "deny"
    assert store.check_action("contact", marca="hotel").decision == "deny"
    assert store.check_action("modify_protected", marca="hermes-core").decision == "gate"
    store.create_brand("zephyr", "Zephyr", por="dep-marca")
    assert store.check_action("publish", marca="zephyr").decision == "allow"
    assert store.check_action("contact", marca="zephyr").decision == "gate"
