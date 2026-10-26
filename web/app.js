const $ = (id) => document.getElementById(id);
const state = { csrf: '', user: null, sources: [], traces: [], selected: null, busy: false, epoch: 0 };
const labels = { evidencia: 'Con evidencia', recuperacion: 'Fragmentos recuperados', abstencion: 'Información insuficiente', conflicto: 'Conflicto entre fuentes', error: 'Servicio o validación' };
const pretty = (value) => JSON.stringify(value, null, 2);
function node(tag, text, cls) { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (cls) n.className = cls; return n; }
async function api(path, options = {}) {
  const response = await fetch(path, { credentials: 'same-origin', ...options, headers: { 'Content-Type': 'application/json', 'X-MIRA-CSRF': state.csrf, ...options.headers } });
  let data; try { data = await response.json(); } catch { throw new Error('El servicio no respondió correctamente. No se generó una respuesta.'); }
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'La solicitud no cumple los datos requeridos.');
  return data;
}
function post(path, body = {}) { return api(path, { method: 'POST', body: JSON.stringify(body) }); }
function setBusy(value) { state.busy = value; $('send-button').disabled = value; $('search-button').disabled = value; }
function addTrace(items = []) { state.traces.push(...items); renderTraces(); }
function renderTraces() {
  $('trace-count').textContent = state.traces.length; $('trace-list').replaceChildren();
  for (const trace of [...state.traces].reverse()) {
    const detail = node('details', undefined, 'trace-card');
    detail.append(node('summary', `${trace.ok ? '✓' : '!' } ${trace.herramienta}`));
    detail.append(node('small', `${trace.fecha} · ${trace.id || trace.traza_id}`));
    detail.append(node('pre', pretty({ argumentos: trace.argumentos, resultado: trace.resultado })));
    $('trace-list').append(detail);
  }
}
function showSources(items = []) {
  state.sources = items; $('source-count').textContent = items.length; $('source-list').replaceChildren();
  if (!items.length) $('source-list').append(node('p', 'No hay citas verificadas en esta respuesta.', 'empty-hint'));
  for (const source of items) {
    const button = node('button', undefined, 'source-card');
    button.append(node('span', `${source.codigo} · v${source.version}`, 'tag'));
    button.append(node('h3', source.seccion));
    button.append(node('p', source.texto.slice(0, 130) + (source.texto.length > 130 ? '…' : '')));
    button.append(node('p', `${source.estado} · Abrir fragmento ↗`, 'meta'));
    button.addEventListener('click', () => openSource(source)); $('source-list').append(button);
  }
}
function openSource(source) {
  $('dialog-kicker').textContent = `${source.codigo} · VERSIÓN ${source.version} · ${source.estado.toUpperCase()}`;
  $('dialog-title').textContent = source.seccion;
  $('dialog-meta').textContent = `${source.fuente} · ${source.vigencia} · ${source.id}`;
  $('dialog-body').textContent = source.texto; $('source-dialog').showModal();
}
function message(role, text, result) {
  $('welcome').hidden = true;
  const wrap = node('article', undefined, `message ${role}`), label = node('div', role === 'user' ? 'Tú' : (result?.autor || 'MIRA · Bonsai'), 'message-label');
  if (result) label.append(node('span', labels[result.estado] || result.estado, `message-state ${result.estado}`));
  wrap.append(label, node('div', text, 'message-text'));
  if (result?.citas?.length) {
    const links = node('div', undefined, 'citation-links');
    for (const source of result.citas) { const b = node('button', `${source.codigo} §${source.seccion.split('.')[0]} · v${source.version}`, 'citation-link'); b.addEventListener('click', () => openSource(source)); links.append(b); }
    wrap.append(links);
  }
  $('conversation').append(wrap); wrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
async function ask(documentOnly = false) {
  const question = $('question').value.trim(); if (state.busy || question.length < 3) return;
  const epoch = state.epoch;
  setBusy(true); $('app-error').textContent = ''; message('user', question); $('question').value = '';
  const busy = node('p', documentOnly ? 'Buscando fragmentos del corpus…' : 'Bonsai está consultando la evidencia y las herramientas…', 'busy'); $('conversation').append(busy);
  try {
    if (documentOnly) {
      const result = await post('/api/buscar', { pregunta: question }); if (epoch !== state.epoch) return; addTrace(result.trazas);
      if (!result.ok) throw new Error(result.error);
      const sources = [...result.datos.fragmentos, ...(result.datos.complementarios_conflicto || [])];
      showSources(sources);
      message('assistant', 'Consulta documental directa: abre los fragmentos recuperados para revisar su contenido. Esta vista no es una respuesta generada por el modelo.', { autor: 'MIRA · Consulta documental', estado: result.datos.conflictos.some(c => c.obligatorio) ? 'conflicto' : 'recuperacion', citas: sources });
    } else {
      const result = await post('/api/chat', { pregunta: question });
      if (epoch !== state.epoch) return;
      addTrace(result.trazas); showSources(result.citas); message('assistant', result.respuesta, result);
      for (const proposal of result.propuestas || []) renderProposal(proposal);
    }
  } catch (error) { if (epoch === state.epoch) message('assistant', error.message, { estado: 'error' }); }
  finally { busy.remove(); if (epoch === state.epoch) { setBusy(false); $('question').focus(); } }
}
async function loadCases() {
  const epoch = state.epoch;
  $('case-list').replaceChildren(node('p', 'Consultando MCP…', 'small'));
  try {
    const result = await api('/api/casos'); if (epoch !== state.epoch) return; addTrace(result.trazas); $('case-list').replaceChildren();
    if (!result.ok) { $('case-list').append(node('p', result.error, 'small')); return; }
    for (const item of result.datos) {
      const button = node('button', undefined, 'case-button' + (item.caso_id === state.selected ? ' active' : ''));
      button.dataset.caseId = item.caso_id; button.append(node('span', '', `case-dot ${item.estado}`));
      const title = node('div'); title.append(node('strong', item.caso_id), node('small', item.estado.replaceAll('_', ' '))); button.append(title);
      button.addEventListener('click', () => selectCase(item.caso_id)); $('case-list').append(button);
    }
  } catch (error) { if (epoch === state.epoch) $('case-list').replaceChildren(node('p', error.message, 'small')); }
}
async function selectCase(id) {
  const epoch = state.epoch;
  $('app-error').textContent = ''; state.selected = id;
  document.querySelectorAll('.case-button').forEach((b) => b.classList.toggle('active', b.dataset.caseId === id));
  const area = $('case-detail'); area.hidden = false; area.replaceChildren(node('p', 'Consultando ficha por MCP…', 'muted'));
  try {
    const response = await api('/api/casos/' + encodeURIComponent(id)); if (epoch !== state.epoch) return; addTrace(response.trazas);
    if (!response.ok) throw new Error(response.error);
    const data = response.datos, record = data.caso;
    area.replaceChildren(node('h2', `${id} · ${record.tipo_proceso.replaceAll('_', ' ')}`));
    area.append(node('p', `${record.estado_actual.replaceAll('_', ' ')} · Puntaje reportado: ${record.puntaje} · Vence: ${record.vence_el || 'No informado'}`, 'case-meta'));
    area.append(node('p', record.motivo_derivacion || 'No se informó un motivo de derivación en el kit.'));
    for (const warning of data.discrepancias) area.append(node('p', `${warning.cambio}: ${warning.descripcion}`, 'discrepancy'));
    const details = node('details'); details.append(node('summary', 'Ver componentes, señales y evidencias'));
    const groups = node('div', undefined, 'signal-groups');
    for (const [title, prefixes] of [['Autenticidad documental', ['DOC_', 'META_']], ['Coherencia biométrica', ['BIO_']], ['Cruce entre fuentes', ['CRUCE_']], ['Señales de fraude', ['FRA_']]]) {
      const group = node('div', undefined, 'signal-group'); group.append(node('h3', title));
      const signals = data.senales.filter((s) => prefixes.some((prefix) => s.codigo.startsWith(prefix)));
      for (const s of signals) group.append(node('p', `${s.codigo}: ${s.valor ?? (s.activa || 'Sin valor')} ${s.minimo === null ? '' : ' / mínimo ' + s.minimo}`, (s.bajo_minimo === 'sí' || s.activa === 'sí') ? 'bad' : ''));
      if (!signals.length) group.append(node('p', 'Sin señales informadas.'));
      groups.append(group);
    }
    details.append(groups, node('p', 'El kit no proporciona pesos ni desglose numérico del puntaje por componente.', 'muted small'));
    for (const evidence of data.evidencias) { details.append(node('p', `${evidence.evidencia_id} · ${evidence.nombre_archivo}: ${evidence.texto_extraido}`, 'small')); if (evidence.alerta_manipulacion) details.append(node('p', evidence.alerta_manipulacion, 'discrepancy')); }
    area.append(details);
    const prepare = node('button', 'Preparar solicitud de antecedentes', 'secondary');
    prepare.addEventListener('click', () => { $('proposal-case').value = id; $('proposal-error').textContent = ''; $('proposal-dialog').showModal(); }); area.append(prepare);
    $('question').value = `¿Por qué se derivó el caso ${id}, qué señales y umbrales lo explican y qué dice la política de decisión?`;
  } catch (error) { if (epoch === state.epoch) area.replaceChildren(node('p', error.message, 'error')); }
}
function renderProposal(proposal) {
  const id = proposal.accion_id; if (document.getElementById(id)) return;
  const card = node('article', undefined, 'proposal-card'); card.id = id;
  card.append(node('p', 'PENDIENTE DE TU CONFIRMACIÓN', 'eyebrow'), node('h3', `Solicitud para ${proposal.caso_id}`), node('p', `Documentos: ${proposal.documentos_solicitados}`), node('p', `Motivo: ${proposal.motivo}`), node('p', 'Al confirmar se registrará una solicitud y cambiará el estado mediante un evento. El aviso al sistema de origen es simulado. La propuesta vence en 10 minutos.', 'muted small'));
  const label = node('label'), check = document.createElement('input'); check.type = 'checkbox'; label.append(check, node('span', 'He revisado el contenido y confirmo expresamente esta solicitud.'));
  const confirm = node('button', 'Confirmar y registrar', 'primary'), cancel = node('button', 'Descartar', 'secondary'); confirm.disabled = true;
  check.addEventListener('change', () => { confirm.disabled = !check.checked; });
  confirm.addEventListener('click', async () => {
    confirm.disabled = true; cancel.disabled = true;
    try { const result = await post(`/api/propuestas/${encodeURIComponent(id)}/confirmar`, { confirmo: true }); addTrace(result.trazas); if (!result.ok) throw new Error(result.error); card.replaceChildren(node('h3', 'Solicitud registrada'), node('p', `${result.datos.solicitud_id} · ${result.datos.caso_id} · ${result.datos.estado}`), node('p', result.datos.aviso_origen, 'muted small')); await loadCases(); if (state.selected) await selectCase(state.selected); }
    catch (error) { card.append(node('p', error.message, 'error')); confirm.disabled = !check.checked; cancel.disabled = false; }
  });
  cancel.addEventListener('click', async () => { try { const result = await post(`/api/propuestas/${encodeURIComponent(id)}/cancelar`); addTrace(result.trazas); if (!result.ok) throw new Error(result.error); card.remove(); } catch (error) { card.append(node('p', error.message, 'error')); } });
  card.append(label, confirm, cancel); $('proposals').append(card);
}
async function enter(data) {
  state.epoch++; setBusy(false);
  state.user = data.usuario; state.csrf = data.csrf; state.selected = null; state.traces = []; state.sources = [];
  $('login-view').hidden = true; $('app-view').hidden = false;
  const names = { 'ORG-01': 'Seguros Cordillera Austral', 'ORG-02': 'Clínica Bahía Serena', 'ORG-03': 'Banco Mirador del Sur' };
  $('org-name').textContent = names[state.user.org_id] || state.user.org_id;
  $('user-name').textContent = `${state.user.nombre} · ${state.user.rol.replaceAll('_', ' ')}`;
  for (const message of document.querySelectorAll('.message')) message.remove(); $('welcome').hidden = false; $('case-detail').hidden = true; $('proposals').replaceChildren(); showSources([]); renderTraces();
  await loadCases();
  try { const result = await api('/api/propuestas'); addTrace(result.trazas); if (result.ok) for (const proposal of result.datos) renderProposal(proposal); } catch {}
  await refreshStatus();
}
async function refreshStatus() { try { const status = await api('/api/status'); const available = status.modelo.disponible; $('model-status').classList.toggle('offline', !available); $('model-status').textContent = available ? `Bonsai local · conectado` : 'Bonsai sin conexión'; $('model-status').title = status.modelo.mensaje || status.modelo.modelos.join(', '); } catch { $('model-status').textContent = 'Servicio no disponible'; } }
$('login-form').addEventListener('submit', async (event) => { event.preventDefault(); const button = event.submitter; button.disabled = true; $('login-error').textContent = ''; try { await enter(await post('/api/login', { usuario_id: $('usuario').value, password: $('password').value })); } catch (error) { $('login-error').textContent = error.message; } finally { button.disabled = false; } });
$('chat-form').addEventListener('submit', (event) => { event.preventDefault(); ask(); });
$('question').addEventListener('keydown', (event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); ask(); } });
$('search-button').addEventListener('click', () => ask(true));
document.querySelectorAll('[data-question]').forEach((button) => button.addEventListener('click', () => { $('question').value = button.dataset.question; $('question').focus(); }));
$('close-dialog').addEventListener('click', () => $('source-dialog').close());
$('close-proposal').addEventListener('click', () => $('proposal-dialog').close());
$('refresh-cases').addEventListener('click', loadCases);
$('logout').addEventListener('click', async () => { try { await post('/api/logout'); } finally { state.csrf = ''; state.user = null; $('app-view').hidden = true; $('login-view').hidden = false; } });
$('sources-tab').addEventListener('click', () => { $('source-list').hidden = false; $('trace-list').hidden = true; $('sources-tab').classList.add('active'); $('traces-tab').classList.remove('active'); $('sources-tab').setAttribute('aria-selected', 'true'); $('traces-tab').setAttribute('aria-selected', 'false'); });
$('traces-tab').addEventListener('click', () => { $('source-list').hidden = true; $('trace-list').hidden = false; $('traces-tab').classList.add('active'); $('sources-tab').classList.remove('active'); $('sources-tab').setAttribute('aria-selected', 'false'); $('traces-tab').setAttribute('aria-selected', 'true'); });
$('all-traces').addEventListener('click', async () => { try { const result = await api('/api/trazas'); if (!result.ok) throw new Error(result.error); state.traces = result.datos.reverse(); renderTraces(); $('traces-tab').click(); } catch (error) { $('app-error').textContent = error.message; } });
$('corpus-button').addEventListener('click', async () => { try { const docs = await api('/api/corpus'); $('dialog-kicker').textContent = 'INVENTARIO DEL CORPUS'; $('dialog-title').textContent = 'Documentos del CU-1'; $('dialog-meta').textContent = 'Incluye versiones derogadas para comparación histórica; la recuperación predeterminada usa solo vigentes.'; $('dialog-body').textContent = docs.map((d) => `${d.codigo} · v${d.version} · ${d.estado}\n${d.titulo}\n${d.vigencia}\n${d.tokens_aproximados} tokens aprox. · ${d.fuente}`).join('\n\n'); $('source-dialog').showModal(); } catch (error) { $('app-error').textContent = error.message; } });
$('proposal-form').addEventListener('submit', async (event) => { event.preventDefault(); event.submitter.disabled = true; $('proposal-error').textContent = ''; try { const result = await post('/api/propuestas', { caso_id: $('proposal-case').value, documentos: $('documents').value, motivo: $('reason').value }); addTrace(result.trazas); if (!result.ok) throw new Error(result.error); renderProposal(result.datos); $('proposal-dialog').close(); $('documents').value = ''; $('reason').value = ''; } catch (error) { $('proposal-error').textContent = error.message; } finally { event.submitter.disabled = false; } });
(async () => { try { const list = await api('/api/usuarios'); for (const user of list) { const option = node('option', `${user.usuario_id} · ${user.nombre} · ${user.org_id}`); option.value = user.usuario_id; $('usuario').append(option); } try { await enter(await api('/api/session')); } catch {} } catch (error) { $('login-error').textContent = error.message; } })();
