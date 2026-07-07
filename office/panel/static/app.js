/* Panel de la oficina Hermes — sin dependencias, sin build. */
"use strict";

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
}[c]));

let SNAP = null;          // último snapshot /api/estado
let ACTIVE_TAB = "panel";
let DRAWER_TASK = null;   // id de tarea abierta en el drawer

const STATE_LABEL = {
  intake: "Intake", queued: "Cola", running: "En curso", gate: "Gate",
  review: "Revisión", blocked: "Bloqueada", done: "Hecha", archived: "Archivada",
};
const KANBAN_COLS = ["intake", "queued", "running", "gate", "review", "blocked", "done"];

// ---------- API ------------------------------------------------------------
function token() { return localStorage.getItem("panel_token") || ""; }

async function api(path, opts = {}) {
  const res = await fetch(path, {
    ...opts,
    headers: {
      "Authorization": "Bearer " + token(),
      "Content-Type": "application/json",
      ...(opts.headers || {}),
    },
  });
  if (res.status === 401) { showLogin(true); throw new Error("401"); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || data.detail || res.statusText);
  return data;
}

async function act(path, body, okMsg) {
  try {
    await api(path, { method: "POST", body: JSON.stringify(body || {}) });
    if (okMsg) toast(okMsg);
    await refresh();
  } catch (e) {
    if (e.message !== "401") toast(e.message, true);
  }
}

// ---------- login / toast ----------------------------------------------------
function showLogin(errored) {
  $("#login").classList.remove("hidden");
  $("#login-error").classList.toggle("hidden", !errored);
}
$("#token-save").addEventListener("click", async () => {
  localStorage.setItem("panel_token", $("#token-input").value.trim());
  try {
    await api("/api/estado");
    $("#login").classList.add("hidden");
    await refresh();
  } catch { showLogin(true); }
});
$("#token-input").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#token-save").click(); });

let toastTimer = null;
function toast(msg, isErr) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.toggle("err", !!isErr);
  t.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.add("hidden"), 4200);
}

// ---------- helpers ----------------------------------------------------------
function ago(iso) {
  if (!iso) return "—";
  const s = (Date.now() - Date.parse(iso)) / 1000;
  if (s < 90) return Math.round(s) + " s";
  if (s < 5400) return Math.round(s / 60) + " min";
  if (s < 172800) return Math.round(s / 3600) + " h";
  return Math.round(s / 86400) + " d";
}
function taskCard(t) {
  return `<div class="task" data-task="${esc(t.id)}">
    <span class="tid">${esc(t.id)}</span> ${esc(t.titulo)}
    <div class="meta">
      ${t.dept ? `<span class="tag">${esc(t.dept)}</span>` : ""}
      <span class="tag prio${t.prioridad}">P${t.prioridad}</span>
      <span class="tag risk-${esc(t.riesgo)}">${esc(t.riesgo)}</span>
      ${t.marca ? `<span class="tag brand">${esc(t.marca)}</span>` : ""}
      ${t.origen === "proactivo" ? `<span class="tag proactivo">proactiva</span>` : ""}
      ${t.agente ? `<span class="tag">🤖 ${esc(t.agente)}</span>` : ""}
    </div></div>`;
}

// ---------- render: cabecera ---------------------------------------------------
function renderHeader() {
  const c = SNAP.control || {};
  const chips = [];
  if (c.kill) chips.push(`<span class="chip err">■ KILL ACTIVO</span>`);
  else if (c.pausa_global) chips.push(`<span class="chip warn">⏸ pausa global</span>`);
  else chips.push(`<span class="chip ok">● operativa</span>`);
  chips.push(`<span class="chip info">🤖 ${SNAP.agentes_en_trabajo.length} en trabajo</span>`);
  chips.push(`<span class="chip ${SNAP.gates_pendientes.length ? "warn" : ""}">⛩ ${SNAP.gates_pendientes.length} gates</span>`);
  chips.push(`<span class="chip">${(SNAP.gasto_mes_eur || 0).toFixed(2)} € / ${c.presupuesto_mes_eur ?? "—"} €${c.freeze_gasto ? " · FREEZE" : ""}</span>`);
  $("#status-chips").innerHTML = chips.join("");

  const badge = $("#gate-badge");
  badge.textContent = SNAP.gates_pendientes.length;
  badge.classList.toggle("hidden", !SNAP.gates_pendientes.length);

  const pauseBtn = $("#btn-pause");
  pauseBtn.textContent = c.pausa_global ? "▶ Reanudar" : "⏸ Pausar";
  pauseBtn.onclick = () => act("/api/control",
    { pausa_global: !c.pausa_global, motivo: "desde el panel" },
    c.pausa_global ? "Oficina reanudada" : "Pausa global activada");

  const killBtn = $("#btn-kill");
  killBtn.textContent = c.kill ? "▶ Rearmar" : "■ KILL";
  killBtn.onclick = () => {
    const q = c.kill ? "¿Rearmar la oficina (quitar kill switch)?"
      : "KILL SWITCH: para TODO el trabajo de la oficina. ¿Seguro?";
    if (confirm(q)) act("/api/control", { kill: !c.kill, motivo: "kill switch panel" },
      c.kill ? "Oficina rearmada" : "KILL activado");
  };
}

// ---------- render: pestaña Panel ------------------------------------------------
function renderPanel() {
  const depts = SNAP.departamentos || {};
  const counts = SNAP.conteo_por_dept || {};
  let html = `<div class="grid">`;
  for (const [slug, d] of Object.entries(depts)) {
    const c = counts[slug] || {};
    const running = SNAP.agentes_en_trabajo.filter((a) => a.dept === slug);
    const pulseDue = (SNAP.pulsos_pendientes || []).includes(slug);
    html += `<div class="card">
      <h3><span class="dot ${d.pausado ? "paused" : (running.length ? "on" : "off")}"></span>
          ${esc(d.nombre)} ${d.orquestador ? '<span class="tag">orquestador</span>' : ""}</h3>
      <div class="mission">${esc(d.mision)}</div>
      ${d.pausado ? `<div class="paused-banner">⏸ En pausa: ${esc(d.pausado_motivo || "")}</div>` : ""}
      <div class="counts">
        <span class="tag">cola ${c.queued || 0}</span>
        <span class="tag">curso ${c.running || 0}</span>
        <span class="tag">gate ${c.gate || 0}</span>
        <span class="tag">rev ${c.review || 0}</span>
        ${c.blocked ? `<span class="tag risk-R2">bloq ${c.blocked}</span>` : ""}
      </div>
      ${running.map((r) => `<div class="note">🤖 ${esc(r.agente)} — ${esc(r.tarea)}: ${esc(r.titulo)} <span class="lbl">(${ago(r.desde)})</span></div>`).join("")}
      <div class="actions">
        ${d.orquestador ? "" : (d.pausado
          ? `<button class="btn sm" data-dept-act="reanudar" data-slug="${slug}">▶ Reanudar</button>`
          : `<button class="btn sm ghost" data-dept-act="pausar" data-slug="${slug}">⏸ Pausar</button>`)}
        ${d.orquestador ? "" : `<button class="btn sm ${pulseDue ? "primary" : ""}" data-dept-act="pulso-ahora" data-slug="${slug}">⚡ Pulso ahora</button>`}
        ${d.orquestador ? "" : `<span class="tag" title="cadencia del pulso proactivo">cada ${Math.round((d.cadencia_min || 0) / 60)} h · WIP ${d.wip}</span>`}
      </div>
    </div>`;
  }
  html += `</div>`;

  const gp = SNAP.gates_pendientes || [];
  if (gp.length) {
    html += `<div class="section-title">Gates esperándote</div>`;
    html += gp.map(gateCard).join("");
  }
  const intake = (SNAP.tareas || []).filter((t) => t.estado === "intake");
  if (intake.length) {
    html += `<div class="section-title">Intake pendiente de triaje (próximo despacho del orquestador)</div>`;
    html += intake.map(taskCard).join("");
  }
  $("#tab-panel").innerHTML = html;
}

// ---------- render: pestaña Tareas -------------------------------------------------
function renderTareas() {
  const tasks = SNAP.tareas || [];
  let html = `<div class="kanban">`;
  for (const st of KANBAN_COLS) {
    const list = tasks.filter((t) => t.estado === st);
    html += `<div class="col"><h4>${STATE_LABEL[st]} <span>${list.length}</span></h4>
      ${list.map(taskCard).join("") || `<div class="empty">—</div>`}</div>`;
  }
  html += `</div>`;
  $("#tab-tareas").innerHTML = html;
}

// ---------- render: pestaña Gates ---------------------------------------------------
function gateCard(g, hist) {
  return `<div class="gate-card ${hist ? "gate-hist" : ""}">
    <h4>[GATE ${esc(g.riesgo)}] ${esc(g.id)} · ${esc(g.tipo)} · tarea ${esc(g.tarea)}${hist ? ` · ${esc(g.estado).toUpperCase()}` : ""}</h4>
    <p><span class="lbl">Qué:</span> ${esc(g.que)}</p>
    <p><span class="lbl">Por qué:</span> ${esc(g.porque || "—")}</p>
    <p><span class="lbl">Rollback:</span> ${esc(g.rollback)}</p>
    ${g.nota_decision ? `<p><span class="lbl">Decisión:</span> ${esc(g.nota_decision)} <span class="lbl">(${ago(g.decidido)})</span></p>` : ""}
    ${hist ? "" : `<div class="actions">
      <button class="btn sm primary" data-gate="${esc(g.id)}" data-dec="aprobado">APRUEBO</button>
      <button class="btn sm danger" data-gate="${esc(g.id)}" data-dec="rechazado">RECHAZO</button>
      <button class="btn sm ghost" data-task="${esc(g.tarea)}">ver tarea</button>
    </div>`}
  </div>`;
}
function renderGates() {
  const p = SNAP.gates_pendientes || [];
  const rec = (SNAP.gates_recientes || []).filter((g) => g.estado !== "pendiente");
  $("#tab-gates").innerHTML =
    (p.length ? p.map((g) => gateCard(g, false)).join("")
      : `<div class="empty">No hay gates pendientes. Silencio = nada esperándote.</div>`)
    + (rec.length ? `<div class="section-title">Decididos recientemente</div>` + rec.map((g) => gateCard(g, true)).join("") : "");
}

// ---------- render: pestaña Marcas ---------------------------------------------------
function renderMarcas() {
  const brands = SNAP.marcas || {};
  let rows = "";
  for (const [slug, b] of Object.entries(brands)) {
    rows += `<tr><td><code>${esc(slug)}</code></td><td>${esc(b.nombre)}</td>
      <td><span class="pill ${esc(b.status)}">${b.status === "protected" ? "protegida" : b.status === "office" ? "de oficina" : esc(b.status)}</span>
          ${b.enforcement === "deny" ? '<span class="pill protected">prohibida</span>' : ""}</td>
      <td class="lbl">${esc(b.notas)}</td><td>${esc(b.creada_por)}</td></tr>`;
  }
  $("#tab-marcas").innerHTML = `
    <table><thead><tr><th>slug</th><th>nombre</th><th>estado</th><th>notas</th><th>creada por</th></tr></thead>
    <tbody>${rows}</tbody></table>
    <div class="section-title">Registrar marca</div>
    <div class="card"><div class="form-row">
      <input id="brand-slug" placeholder="slug (minúsculas-y-guiones)">
      <input id="brand-name" placeholder="Nombre">
      <select id="brand-status"><option value="office">de oficina (autónoma)</option><option value="protected">protegida (solo gate)</option></select>
      <input id="brand-notes" placeholder="notas / carta de marca" style="flex:1">
      <button class="btn primary" id="brand-create">Registrar</button>
    </div>
    <p class="lbl" style="font-size:.8rem">Protegida = la oficina jamás publica ni toca nada en su nombre sin tu APRUEBO. De oficina = los departamentos pueden operar y publicar bajo ella con compliance.</p>
    </div>`;
  $("#brand-create").onclick = () => act("/api/marcas", {
    slug: $("#brand-slug").value, nombre: $("#brand-name").value,
    status: $("#brand-status").value, notas: $("#brand-notes").value,
  }, "Marca registrada");
}

// ---------- render: pestaña Actividad ---------------------------------------------------
function renderActividad() {
  const evs = SNAP.eventos || [];
  $("#tab-actividad").innerHTML = `<ul class="feed">` + evs.map((e) => `
    <li><span class="ts">${esc((e.ts || "").replace("T", " ").replace("Z", ""))}</span>
        <span class="k"><span class="tag">${esc(e.tipo)}</span></span>
        <span><b>${esc(e.actor)}</b> — ${esc(e.mensaje)}${e.ref ? ` <code>${esc(e.ref)}</code>` : ""}</span></li>`).join("")
    + `</ul>`;
  $$("#tab-actividad code").forEach((c) => {
    if (/^T-\d+/.test(c.textContent)) {
      c.style.cursor = "pointer";
      c.addEventListener("click", () => openDrawer(c.textContent));
    }
  });
}

// ---------- render: pestaña Sistema ---------------------------------------------------
function renderSistema() {
  const c = SNAP.control || {};
  $("#tab-sistema").innerHTML = `<div class="sys-grid">
    <div class="card"><h3>Límites de trabajo</h3>
      <label>WIP global (agentes ejecutando a la vez)</label>
      <input id="sys-wip" type="number" min="1" max="8" value="${c.wip_global ?? 2}">
      <div class="form-row"><button class="btn sm" id="sys-save-wip">Guardar</button></div>
    </div>
    <div class="card"><h3>Presupuesto (€ reales)</h3>
      <label>Techo mensual</label><input id="sys-budget" type="number" value="${c.presupuesto_mes_eur ?? 100}">
      <label>Límite autónomo por tarea</label><input id="sys-limit" type="number" value="${c.limite_tarea_eur ?? 20}">
      <div class="form-row"><button class="btn sm" id="sys-save-budget">Guardar</button>
      ${c.freeze_gasto ? `<button class="btn sm danger" id="sys-unfreeze">Quitar FREEZE de gasto</button>` : ""}</div>
      <p class="lbl" style="font-size:.8rem">Gasto este mes: ${(SNAP.gasto_mes_eur || 0).toFixed(2)} €. El freeze salta solo al 80% del techo.</p>
    </div>
    <div class="card"><h3>Estado del sustrato</h3>
      <p style="font-size:.85rem">La agencia corre en el daemon <b>Hermes Agent</b> de la VM (skills + cron + subagentes). Este panel solo lee y escribe el tablero (<code>~/office/state</code>) — el mismo que usan los agentes vía <code>oficina</code>.</p>
      <p style="font-size:.85rem;margin-top:8px" class="lbl">Kill switch de emergencia fuera del panel: <code>systemctl stop hermes</code> en la VM, o «PARA TODO» por Telegram.</p>
      <p style="font-size:.85rem;margin-top:8px" class="lbl">Snapshot: ${esc(SNAP.ts)}</p>
    </div>
  </div>`;
  $("#sys-save-wip").onclick = () => act("/api/control", { wip_global: +$("#sys-wip").value }, "WIP guardado");
  $("#sys-save-budget").onclick = () => act("/api/control", {
    presupuesto_mes_eur: +$("#sys-budget").value, limite_tarea_eur: +$("#sys-limit").value,
  }, "Presupuesto guardado");
  const uf = $("#sys-unfreeze");
  if (uf) uf.onclick = () => act("/api/control", { freeze_gasto: false, motivo: "freeze retirado por el propietario" }, "Freeze retirado");
}

// ---------- drawer de tarea ------------------------------------------------------------
async function openDrawer(tid) {
  let t;
  try { t = await api("/api/tareas/" + tid); } catch (e) { toast(e.message, true); return; }
  DRAWER_TASK = tid;
  const depts = Object.keys(SNAP.departamentos || {}).filter((s) => !(SNAP.departamentos[s] || {}).orquestador);
  const deptOpts = depts.map((d) => `<option value="${d}" ${t.dept === d ? "selected" : ""}>${d}</option>`).join("");
  const gatesOfTask = (SNAP.gates_recientes || []).filter((g) => g.tarea === tid && g.estado === "pendiente");
  $("#drawer-content").innerHTML = `
    <button class="btn sm ghost" id="drawer-close" style="float:right">✕</button>
    <h2><span class="tid">${esc(t.id)}</span> · ${esc(STATE_LABEL[t.estado] || t.estado)}</h2>
    <div class="meta" style="margin:6px 0">
      <span class="tag">${esc(t.dept || "sin dept")}</span><span class="tag prio${t.prioridad}">P${t.prioridad}</span>
      <span class="tag risk-${esc(t.riesgo)}">${esc(t.riesgo)}</span>
      ${t.marca ? `<span class="tag brand">${esc(t.marca)}</span>` : ""}
      <span class="tag">${esc(t.origen)}</span>${t.agente ? `<span class="tag">🤖 ${esc(t.agente)}</span>` : ""}
    </div>
    <h2 style="font-weight:600">${esc(t.titulo)}</h2>
    <div class="desc">${esc(t.descripcion || "(sin descripción)")}</div>
    ${t.resultado ? `<div class="section-title">Resultado</div><div class="desc">${esc(t.resultado)}</div>` : ""}
    ${(t.artefactos || []).length ? `<div class="section-title">Artefactos</div>` +
      t.artefactos.map((a) => `<div class="note">📎 [${esc(a.tipo)}] <code>${esc(a.ref)}</code> ${esc(a.nota || "")}</div>`).join("") : ""}
    ${(t.notas || []).length ? `<div class="section-title">Notas</div>` +
      t.notas.map((n) => `<div class="note"><b>${esc(n.autor)}</b>: ${esc(n.texto)} <span class="lbl">(${ago(n.ts)})</span></div>`).join("") : ""}
    ${gatesOfTask.length ? `<div class="section-title">Gates de esta tarea</div>` + gatesOfTask.map((g) => gateCard(g, false)).join("") : ""}
    <div class="section-title">Actuar</div>
    <div class="form-row"><input id="dw-note" placeholder="nota para el agente / orquestador" style="flex:1">
      <button class="btn sm" id="dw-add-note">Añadir nota</button></div>
    <div class="form-row">
      <select id="dw-dept">${deptOpts}</select>
      <select id="dw-prio">${[1, 2, 3, 4, 5].map((p) => `<option ${p === t.prioridad ? "selected" : ""}>${p}</option>`).join("")}</select>
      ${t.estado === "intake" ? `<button class="btn sm primary" id="dw-assign">Asignar ya (sin esperar al orquestador)</button>`
        : `<button class="btn sm" id="dw-edit">Guardar dept/prioridad</button>`}
    </div>
    <div class="form-row">
      ${["review", "gate", "blocked"].includes(t.estado) ? `<button class="btn sm" id="dw-requeue">↩ Recolar</button>` : ""}
      ${t.estado === "review" ? `<button class="btn sm primary" id="dw-close">✓ Dar por buena</button>` : ""}
      ${t.estado !== "archived" && t.estado !== "done" ? `<button class="btn sm danger" id="dw-archive">🗑 Archivar</button>` : ""}
    </div>
    <div class="section-title">Historial</div>
    <ul class="hist">${(t.historial || []).map((h) => `<li>${esc((h.ts || "").replace("T", " ").replace("Z", ""))} — ${h.de ? esc(h.de) + " → " : ""}${esc(h.a)} (${esc(h.por)})${h.motivo ? ": " + esc(h.motivo) : ""}</li>`).join("")}</ul>`;
  $("#drawer").classList.remove("hidden");
  $("#drawer-backdrop").classList.remove("hidden");
  $("#drawer-close").onclick = closeDrawer;
  $("#dw-add-note").onclick = () => {
    const texto = $("#dw-note").value.trim();
    if (texto) act(`/api/tareas/${tid}/accion`, { accion: "nota", texto }, "Nota añadida").then(() => openDrawer(tid));
  };
  const assign = $("#dw-assign");
  if (assign) assign.onclick = () => act(`/api/tareas/${tid}/accion`,
    { accion: "asignar", dept: $("#dw-dept").value, prioridad: +$("#dw-prio").value }, "Asignada").then(closeDrawer);
  const edit = $("#dw-edit");
  if (edit) edit.onclick = () => act(`/api/tareas/${tid}/accion`,
    { accion: "editar", dept: $("#dw-dept").value, prioridad: +$("#dw-prio").value }, "Guardado").then(() => openDrawer(tid));
  const rq = $("#dw-requeue");
  if (rq) rq.onclick = () => act(`/api/tareas/${tid}/accion`, { accion: "recolar", motivo: "recolada desde el panel" }, "Recolada").then(closeDrawer);
  const cl = $("#dw-close");
  if (cl) cl.onclick = () => act(`/api/tareas/${tid}/accion`, { accion: "cerrar" }, "Cerrada").then(closeDrawer);
  const ar = $("#dw-archive");
  if (ar) ar.onclick = () => {
    const motivo = prompt("Motivo de archivado (matar pronto es éxito):", "no aporta ahora");
    if (motivo !== null) act(`/api/tareas/${tid}/accion`, { accion: "archivar", motivo }, "Archivada").then(closeDrawer);
  };
}
function closeDrawer() {
  DRAWER_TASK = null;
  $("#drawer").classList.add("hidden");
  $("#drawer-backdrop").classList.add("hidden");
}
$("#drawer-backdrop").addEventListener("click", closeDrawer);

// ---------- eventos globales ------------------------------------------------------------
document.body.addEventListener("click", (e) => {
  const taskEl = e.target.closest("[data-task]");
  if (taskEl) { openDrawer(taskEl.dataset.task); return; }
  const gateBtn = e.target.closest("[data-gate]");
  if (gateBtn) {
    const dec = gateBtn.dataset.dec;
    const nota = dec === "rechazado" ? (prompt("Motivo del rechazo:") ?? "") : (prompt("Nota (opcional):") ?? "");
    act(`/api/gates/${gateBtn.dataset.gate}/decidir`, { decision: dec, nota },
      dec === "aprobado" ? "APRUEBO registrado — el orquestador lo retoma en el próximo despacho" : "RECHAZO registrado");
    return;
  }
  const deptBtn = e.target.closest("[data-dept-act]");
  if (deptBtn) {
    const accion = deptBtn.dataset.deptAct;
    const body = { accion };
    if (accion === "pausar") body.motivo = prompt("Motivo de la pausa:", "pausado por el propietario") ?? "";
    act(`/api/departamentos/${deptBtn.dataset.slug}/accion`, body,
      accion === "pulso-ahora" ? "Pulso solicitado: entra en el próximo despacho del orquestador" : "Hecho");
  }
});

$("#intake-send").addEventListener("click", () => {
  const texto = $("#intake-text").value.trim();
  if (!texto) return;
  act("/api/intake", { texto, prioridad: +$("#intake-prio").value },
    "Enviado al orquestador: lo triará en su próximo despacho").then(() => { $("#intake-text").value = ""; });
});
$("#intake-text").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#intake-send").click(); });

$$("#tabs button").forEach((b) => b.addEventListener("click", () => {
  ACTIVE_TAB = b.dataset.tab;
  $$("#tabs button").forEach((x) => x.classList.toggle("active", x === b));
  $$(".tab").forEach((t) => t.classList.add("hidden"));
  $("#tab-" + ACTIVE_TAB).classList.remove("hidden");
  renderActive();
}));

// ---------- ciclo de refresco ------------------------------------------------------------
function renderActive() {
  if (!SNAP) return;
  renderHeader();
  ({ panel: renderPanel, tareas: renderTareas, gates: renderGates,
     marcas: renderMarcas, actividad: renderActividad, sistema: renderSistema }[ACTIVE_TAB])();
}

async function refresh() {
  try {
    SNAP = await api("/api/estado");
    renderActive();
  } catch (e) { /* 401 ya gestionado */ }
}

(async function init() {
  if (!token()) { showLogin(false); return; }
  await refresh();
})();
setInterval(() => { if (token() && !document.hidden) refresh(); }, 4000);
