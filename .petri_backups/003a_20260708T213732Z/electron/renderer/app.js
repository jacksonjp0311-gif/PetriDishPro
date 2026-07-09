const densityCanvas = document.getElementById('densityCanvas');
const curveCanvas = document.getElementById('curveCanvas');
const dctx = densityCanvas.getContext('2d');
const cctx = curveCanvas.getContext('2d');
const runLabel = document.getElementById('runLabel');
const legend = document.getElementById('legend');
const metricsEl = document.getElementById('metrics');
const summaryEl = document.getElementById('summary');
const canvasWrap = document.getElementById('canvasWrap');

let latest = null;
let activeField = 'density';
let zoom = 1;
let panX = 0;
let panY = 0;
let dragging = false;
let dragStart = null;

function colorForValue(v, field) {
  v = Math.max(0, Math.min(1, Number(v) || 0));
  if (field === 'toxin') return [255 * v, 42 * v, 214 * v];
  if (field === 'nutrient') return [255 * v, 170 * v, 20 * v];
  if (field === 'oxygen') return [70 * v, 170 * v, 255 * v];
  if (field === 'waste') return [160 * v, 255 * v, 95 * v];
  const r = Math.min(255, 20 + 30 * v + 80 * Math.pow(v, 3));
  const g = Math.min(255, 70 + 210 * v);
  const b = Math.min(255, 120 + 135 * Math.sqrt(v));
  return [r, g, b];
}

function resizeCanvases() {
  const rect = canvasWrap.getBoundingClientRect();
  densityCanvas.width = Math.max(320, Math.floor(rect.width));
  densityCanvas.height = Math.max(240, Math.floor(rect.height));
  const crect = curveCanvas.getBoundingClientRect();
  curveCanvas.width = Math.max(320, Math.floor(crect.width));
  curveCanvas.height = Math.max(180, Math.floor(crect.height));
  drawAll();
}

function getMatrix() {
  if (!latest) return null;
  if (activeField === 'density') return latest.density?.density?.normalized || latest.run?.density?.normalized;
  return latest.density?.fields?.[activeField] || latest.run?.fields?.[activeField];
}

function drawDensity() {
  const w = densityCanvas.width;
  const h = densityCanvas.height;
  dctx.clearRect(0, 0, w, h);
  dctx.fillStyle = '#020611';
  dctx.fillRect(0, 0, w, h);
  const matrix = getMatrix();
  if (!matrix || !matrix.length) {
    dctx.fillStyle = '#8da8bd';
    dctx.font = '18px Segoe UI';
    dctx.fillText('No density artifact loaded.', 30, 40);
    return;
  }
  const n = matrix.length;
  const base = Math.min(w, h) * 0.92 * zoom;
  const cell = base / n;
  const ox = (w - base) / 2 + panX;
  const oy = (h - base) / 2 + panY;

  dctx.save();
  dctx.beginPath();
  dctx.arc(w / 2, h / 2, Math.min(w, h) * 0.47, 0, Math.PI * 2);
  dctx.clip();
  for (let y = 0; y < n; y++) {
    const row = matrix[y];
    for (let x = 0; x < row.length; x++) {
      const v = row[x];
      if (v <= 0.002) continue;
      const [r, g, b] = colorForValue(v, activeField);
      dctx.fillStyle = `rgba(${r|0},${g|0},${b|0},${Math.min(0.95, 0.16 + v * 0.95)})`;
      dctx.fillRect(ox + x * cell, oy + y * cell, Math.ceil(cell + 0.5), Math.ceil(cell + 0.5));
    }
  }
  // Glass lens vignette.
  const grad = dctx.createRadialGradient(w/2, h/2, Math.min(w,h)*0.12, w/2, h/2, Math.min(w,h)*0.50);
  grad.addColorStop(0, 'rgba(255,255,255,0.04)');
  grad.addColorStop(0.62, 'rgba(0,240,255,0.03)');
  grad.addColorStop(1, 'rgba(0,0,0,0.66)');
  dctx.fillStyle = grad;
  dctx.fillRect(0, 0, w, h);
  dctx.restore();

  dctx.strokeStyle = 'rgba(0,240,255,0.20)';
  dctx.lineWidth = 2;
  dctx.beginPath();
  dctx.arc(w/2, h/2, Math.min(w,h)*0.47, 0, Math.PI*2);
  dctx.stroke();
}

function drawCurves() {
  const w = curveCanvas.width;
  const h = curveCanvas.height;
  cctx.clearRect(0, 0, w, h);
  cctx.fillStyle = '#030814';
  cctx.fillRect(0, 0, w, h);
  const curves = latest?.run?.curves || [];
  const organisms = latest?.run?.organisms || [];
  if (!curves.length || !organisms.length) return;
  const pad = 28;
  let maxPop = 1;
  organisms.forEach(o => {
    curves.forEach(row => { maxPop = Math.max(maxPop, Number(row[o.id]) || 0); });
  });
  cctx.strokeStyle = 'rgba(255,255,255,.10)';
  cctx.lineWidth = 1;
  for (let i=0; i<5; i++) {
    const y = pad + i * (h - pad * 2) / 4;
    cctx.beginPath(); cctx.moveTo(pad, y); cctx.lineTo(w - pad, y); cctx.stroke();
  }
  organisms.forEach(o => {
    cctx.strokeStyle = o.color || '#00f0ff';
    cctx.lineWidth = 2;
    cctx.beginPath();
    curves.forEach((row, i) => {
      const x = pad + (i / Math.max(1, curves.length - 1)) * (w - pad * 2);
      const y = h - pad - ((Number(row[o.id]) || 0) / maxPop) * (h - pad * 2);
      if (i === 0) cctx.moveTo(x, y); else cctx.lineTo(x, y);
    });
    cctx.stroke();
  });
  cctx.fillStyle = '#8da8bd';
  cctx.font = '11px Segoe UI';
  cctx.fillText('population', 8, 14);
  cctx.fillText('step', w - 48, h - 8);
}

function renderLegend() {
  legend.innerHTML = '';
  const organisms = latest?.run?.organisms || [];
  organisms.forEach(o => {
    const item = document.createElement('div');
    item.className = 'legendItem';
    item.innerHTML = `<span class="swatch" style="background:${o.color}; color:${o.color}"></span><span>${o.label}</span>`;
    legend.appendChild(item);
  });
}

function renderMetrics() {
  metricsEl.innerHTML = '';
  const m = latest?.run?.metrics || {};
  const keys = ['final_total_population', 'final_max_density', 'nutrient_total', 'toxin_total', 'waste_total', 'organism_count'];
  keys.forEach(k => {
    const div = document.createElement('div');
    div.className = 'metric';
    div.innerHTML = `${k.replaceAll('_', ' ')}<b>${m[k] ?? '—'}</b>`;
    metricsEl.appendChild(div);
  });
}

function renderSummary() {
  const validation = latest?.validation;
  const run = latest?.run;
  if (!run) {
    summaryEl.textContent = 'No run loaded.';
    return;
  }
  summaryEl.textContent = [
    `Run: ${run.run_id}`,
    `Engine: ${run.engine}`,
    `Validation: ${validation?.status || 'unknown'}`,
    '',
    'Boundary:',
    run.claim_boundary,
    '',
    'Organisms:',
    ...(run.organisms || []).map(o => `- ${o.label}: ${o.final_population}`),
    '',
    'Notes:',
    ...(Object.values(run.model_notes || {}).map(v => `- ${v}`))
  ].join('\n');
}

function drawAll() {
  drawDensity();
  drawCurves();
}

async function loadLatest() {
  latest = await window.petri.readLatest();
  if (latest?.run) {
    runLabel.textContent = `${latest.run.experiment.name} · ${latest.run.run_id}`;
  } else {
    runLabel.textContent = 'No run loaded';
  }
  renderLegend();
  renderMetrics();
  renderSummary();
  drawAll();
}

async function runPreset() {
  const preset = document.getElementById('preset').value;
  const grid = Number(document.getElementById('grid').value);
  const steps = Number(document.getElementById('steps').value);
  runLabel.textContent = 'Running simulation...';
  const res = await window.petri.runPreset(preset, { grid, steps });
  if (!res.ok) {
    runLabel.textContent = 'Simulation failed';
    summaryEl.textContent = `${res.stderr || ''}\n${res.stdout || ''}`;
    return;
  }
  await loadLatest();
}

document.getElementById('runBtn').addEventListener('click', runPreset);
document.getElementById('loadBtn').addEventListener('click', loadLatest);
document.querySelectorAll('.fieldBtn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.fieldBtn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeField = btn.dataset.field;
    drawDensity();
  });
});
document.getElementById('zoom').addEventListener('input', (e) => { zoom = Number(e.target.value); drawDensity(); });
document.getElementById('zoomIn').addEventListener('click', () => { zoom = Math.min(8, zoom + 0.3); document.getElementById('zoom').value = zoom; drawDensity(); });
document.getElementById('zoomOut').addEventListener('click', () => { zoom = Math.max(1, zoom - 0.3); document.getElementById('zoom').value = zoom; drawDensity(); });
document.getElementById('resetView').addEventListener('click', () => { zoom = 1; panX = 0; panY = 0; document.getElementById('zoom').value = 1; drawDensity(); });
canvasWrap.addEventListener('mousedown', (e) => { dragging = true; dragStart = { x: e.clientX, y: e.clientY, panX, panY }; });
window.addEventListener('mouseup', () => { dragging = false; });
window.addEventListener('mousemove', (e) => {
  if (!dragging || !dragStart) return;
  panX = dragStart.panX + e.clientX - dragStart.x;
  panY = dragStart.panY + e.clientY - dragStart.y;
  drawDensity();
});
window.addEventListener('resize', resizeCanvases);
resizeCanvases();
loadLatest();
