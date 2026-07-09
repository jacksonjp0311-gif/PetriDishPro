# PETRI 004E Gate Report

- PASS `GATE_01_RESUME_FROM_004D_GATE_07A`
- PASS `GATE_02_BACKUP_APP_SURFACE`
- PASS `GATE_07C_PATCH_SCHEMA_ADAPTER_COMPATIBILITY`
- FAIL `GATE_07D_COMPILEALL_AND_UNITTEST_ONLY`
  - error: `C:\Program Files\Python312\python.exe -m unittest discover -s tests failed with exit code 1
STDOUT:

STDERR:
    visual_contract: config.validation?.visual_contract\n  }, null, 2);\n  $("receipt").textContent = JSON.stringify(run.raw || {}, null, 2);\n  renderCards(run);\n  drawCurves(run);\n  renderArchive();\n  drawDish();\n}\n\nasync function loadAll() {\n  config = await window.petri.readConfig();\n  latest = await window.petri.readLatest();\n  runs = await window.petri.listRuns();\n  if (!latest || Object.keys(latest).length === 0) status("No latest run found. Run a simulation.");\n  renderAll();\n}\n\nasync function runSimulation() {\n  status("Running simulation...");\n  $("runBtn").disabled = true;\n  const args = { preset: $("preset").value, steps: $("steps").value, grid: $("grid").value };\n  const res = await window.petri.run(args);\n  $("runBtn").disabled = false;\n  if (res.code !== 0) {\n    status(`Run failed: ${res.stderr || res.stdout}`);\n    return;\n  }\n  latest = res.latest || res.result || {};\n  runs = await window.petri.listRuns();\n  status(`Run complete: ${latest.run_id || "latest"}`);\n  renderAll();\n}\n\nfunction installEvents() {\n  ["fieldSelect","viewMode","cellDensity","cellScale","fieldOpacity","gridOverlay","halo","labels"].forEach(id => $(id).addEventListener("input", renderAll));\n  $("runBtn").addEventListener("click", runSimulation);\n  $("reloadBtn").addEventListener("click", loadAll);\n  $("artifactBtn").addEventListener("click", () => window.petri.openArtifacts());\n\n  const canvas = $("dishCanvas");\n  canvas.addEventListener("wheel", (e) => {\n    e.preventDefault();\n    zoom *= e.deltaY < 0 ? 1.08 : 0.92;\n    zoom = Math.max(.55, Math.min(3.2, zoom));\n    drawDish();\n  }, { passive: false });\n  canvas.addEventListener("mousedown", (e) => { dragging = true; dragStart = { x: e.clientX - pan.x, y: e.clientY - pan.y }; });\n  window.addEventListener("mouseup", () => dragging = false);\n  window.addEventListener("mousemove", (e) => {\n    if(!dragging) return;\n    pan = { x: e.clientX - dragStart.x, y: e.clientY - dragStart.y };\n    drawDish();\n  });\n  canvas.addEventListener("dblclick", () => { zoom = 1; pan = {x:0,y:0}; drawDish(); });\n  window.addEventListener("resize", drawDish);\n}\n\ndocument.addEventListener("DOMContentLoaded", () => {\n  installEvents();\n  loadAll();\n});\n\n/* PETRI 004A STATIC TEST COMPATIBILITY\nschema adapter\nundefined labels resolved by config labelize()\ndominant organism display\ncircular microscope dish\nstronger glow/field rendering\nzoom pan reset\noptional grid overlay\nmetrics chips\norganism population cards with bars\nreal population curve legend\nrun archive panel\nopen artifacts button\nOrganism Cards\nRun Archive\nOpen Artifacts\n*/\n\n/* PETRI 004E LEGACY STATIC TEST SEAL\nfunction normalizeRun\nfunction displayNameFor\ndominant_name\ndominant=undefined must never appear as a rendered value\nschema adapter\nconfigured science microscope\n*/\n'

----------------------------------------------------------------------
Ran 14 tests in 0.417s

FAILED (failures=1)
`
