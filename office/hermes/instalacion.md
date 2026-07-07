# Instalación de la oficina en el Hermes de la VM

Prerrequisito: F0.B del PLAN completado hasta B7 (Hermes instalado y con al
menos un backend; repo clonado en `~/office/kaikhermes`). Todo lo de abajo es
idempotente y reversible (la VM es desechable).

## 1. Tablero + CLI (determinista)

```bash
cd ~/office/kaikhermes
bash office/deploy.sh          # siembra ~/office/state, enlaza `oficina`, instala el panel
```

`deploy.sh` deja: estado sembrado (departamentos, marcas protegidas, control),
`oficina` en `~/.local/bin`, panel como servicio systemd de usuario en
`127.0.0.1:8787` y el token del panel en `~/.hermes-office/panel.yaml`.

## 2. Skills en Hermes

Las skills viven en el repo (canónicas) y se instalan en el daemon.

**Mecanismo preferente** — clave `skills.external_dirs` de
`${HERMES_HOME:-~/.hermes}/config.yaml` (**[TBV]** confirmar la clave exacta
en tu versión; fuente y confianza: `knowledge/core/agency-agents-hermes.md`).
Apunta al repo directamente, así no hay copia que derive:

```yaml
skills:
  external_dirs:
    - ~/office/kaikhermes/skills/oficina
    - ~/office/kaikhermes/skills/semilla
```

Con 19 skills el catálogo inicial no se infla; es exactamente el caso bueno
de `external_dirs`.

**Fallback** si tu versión no soporta esa clave — symlinks al directorio de
skills del daemon:

```bash
for s in oficina-protocolo orquestador-despacho dep-mercado dep-producto dep-marketing dep-marca; do
  ln -sfn ~/office/kaikhermes/skills/oficina/$s ~/.hermes/skills/$s
done
# Las 13 semilla igual (paso B7 del PLAN), si no estaban ya:
for s in ~/office/kaikhermes/skills/semilla/*/; do ln -sfn "$s" ~/.hermes/skills/$(basename "$s"); done
```

En ambos casos el working copy del repo es la fuente: la retro semanal
audita diffs contra el repo con `git`. El formato de cada SKILL.md lo
protege la suite (`office/tests/test_skills.py`).

## 3. Instrucción permanente del agente raíz (JdG)

Añadir al system prompt / config del daemon (**[TBV]** dónde vive en tu
versión: `~/.hermes/config.yaml` o equivalente):

> Eres el Jefe de Gabinete de la oficina (skill `orquestador-despacho`).
> Todo mensaje del propietario es intake: regístralo con `oficina intake add`
> y ejecuta un ciclo de despacho. El tablero (`oficina`) manda sobre tu
> memoria. PATH incluye ~/.local/bin.

## 4. Cron del daemon

Dar de alta los jobs de `office/hermes/cron.md` con el mecanismo de cron de
Hermes (**[TBV]** sintaxis). Verificar el primero (despacho) viendo aparecer
eventos en el panel.

## 5. Validación (añadir al issue #5, junto al plan doc 09 §8)

- [ ] `oficina estado` funciona para el usuario del daemon y para subagentes.
- [ ] Un subagente aislado ve `oficina` en PATH y el mismo `~/office/state`.
- [ ] Despacho por cron: un intake de prueba queda triado en <20 min sin tocar nada.
- [ ] Pulso proactivo: con el tablero vacío, en <24 h hay tareas `origen: proactivo`.
- [ ] Política: `oficina politica check --accion-externa publish --marca ezti` → exit 3 (GATE);
      `--marca hotel` → exit 4 (DENY); con una marca de oficina de prueba → exit 0.
- [ ] Gate de panel: abrir uno de prueba, APRUEBO desde el panel, el despacho lo retoma.
- [ ] Kill switch del panel: con `kill` activo, `oficina tarea empezar` es rechazado
      y el despacho no arranca nada. Rearme solo desde el panel (owner).
- [ ] El panel NO es alcanzable desde fuera de la VM (curl desde otra máquina falla);
      túnel SSH sí: `ssh -L 8787:127.0.0.1:8787 <vm>` → http://localhost:8787.

## 6. (Opcional, post-B12) Consultores bajo demanda: `agency-agents-router`

ADR-005. ~280 especialistas-prompt (MIT) disponibles como plugin *lazy* de
Hermes: 4 tools (`agency_agents_search/_inspect/_load/_delegate`) que buscan
y cargan especialistas desde disco **sin añadir nada al catálogo de skills**.
No es requisito de ninguna fase; instalar solo si los departamentos lo van a
usar como biblioteca de método.

```bash
git clone https://github.com/msitarzewski/agency-agents ~/office/repos/agency-agents
cd ~/office/repos/agency-agents
git checkout 71394d83e9b5f73ef6e3f044fdc97e95a68f0e59   # commit auditado en ADR-005
./scripts/convert.sh --tool hermes    # genera integrations/hermes/agency-agents-router
./scripts/install.sh --tool hermes    # copia a ~/.hermes/plugins/ y lo añade a plugins.enabled
# reiniciar sesiones/gateway para que el daemon descubra los tools
```

Reglas de uso (las mismas de siempre, explícitas):

- El especialista cargado es **contexto puntual de una tarea**, no una
  skill ni una autoridad: `oficina politica check`, gates R2/R3 y el
  protocolo de la oficina siguen mandando.
- Prohibido añadir el roster a `skills.external_dirs` o copiarlo a
  `skills/` — el catálogo solo crece por el ciclo gobernado.
- Mapa de divisiones útiles por departamento:
  `knowledge/core/agency-agents-hermes.md` §3.

Validación: pedir al raíz «busca un especialista de pricing con el router»
→ debe usar `agency_agents_search` y proponer, no precargar el roster.

Rollback: `rm -rf ~/.hermes/plugins/agency-agents-router` + quitar la línea
de `plugins.enabled` en `~/.hermes/config.yaml`.

## Rollback

`systemctl --user disable --now hermes-office-panel` + quitar
`external_dirs`/symlinks de skills + `rm -rf ~/office/state` (el tablero es
operativo, no institucional; lo institucional está en git). Hermes queda
como estaba.
