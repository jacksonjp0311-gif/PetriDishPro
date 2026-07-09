# Petri Dish Pro Roadmap

## Current baseline — v0.1 standalone organism cockpit

Status: working standalone repo.

Core loop:

```text
Organism preset -> Python grid simulation -> density/field artifacts -> validation receipt -> Electron microscope HUD
```

What is already in the build:

- Pure Python spatial-agent engine.
- Electron microscope cockpit with zoom, pan, density rendering, fields, and population curves.
- Organism presets for microbial competition, antibiotic selection, and cellular tissue interaction.
- Organism library: fast microbe, spore former, yeast-like colony, predator microbe, resistant variant, immune-like cell, infected cell, cancer-like clone.
- Fields: density, nutrient, toxin/antibiotic, oxygen, and waste.
- Validation receipts and reproducible run artifacts.
- Terminal entrypoint: `ORGANISM_GATE.ps1`.

## v0.2 — Organism Gate / Operator Surface

Goal: make the startup experience feel like a biological command portal instead of a plain app launch.

Planned work:

- Add richer terminal dashboard telemetry before Electron launch.
- Add preset status cards: organism count, field pressure, expected interaction type, claim boundary.
- Add "last run" snapshot in the terminal gate.
- Add organism encyclopedia view in Electron.
- Add click-to-inspect cells on the density map.
- Add run comparison: current run versus previous run.

Exit criteria:

- A user can start from `ORGANISM_GATE.ps1`, choose an organism experiment, run it, open the Electron HUD, and inspect the artifact receipt without touching internal files.

## v0.3 — Better Biology Kernels

Goal: move from visually useful toy dynamics to more scientifically structured simulation contracts.

Planned work:

- Add explicit species interaction matrix.
- Add mutation/adaptation events for resistant variants.
- Add dormancy/spore-state switching for stress-tolerant organisms.
- Add biofilm adhesion and local shielding.
- Add chemotaxis toward nutrient hotspots and away from toxin fields.
- Add phage-like predator preset.
- Add symbiosis preset with producer/consumer/cross-feeding dynamics.

Exit criteria:

- Each organism declares not only growth/death/motility, but also interaction rules and state transitions.

## v0.4 — Scientific Artifact Layer

Goal: make every run more auditable and easier to compare.

Planned work:

- Export population curves as CSV.
- Export density snapshots as SVG/PNG.
- Add `experiment.json`, `provenance.json`, and `validation.json` per run.
- Add parameter sweep runner.
- Add batch comparison reports.
- Add scorecard: stability, extinction, dominance, resistance selection, field depletion, waste burden.

Exit criteria:

- Runs are reproducible, comparable, and reviewable without opening the app.

## v0.5 — Dataset and Standards Adapters

Goal: prepare for real scientific inputs without pretending the model is validated.

Planned work:

- CSV adapter for initial population maps and field maps.
- SBML import stub for biochemical reaction models.
- AnnData/h5ad adapter design for future single-cell experiments.
- COMBINE/OMEX and SED-ML export notes.
- Metadata manifest using RO-Crate/PROV-style provenance.

Exit criteria:

- External data can be loaded as bounded inputs with clear claim restrictions.

## v0.6 — Electron Lab Workbench

Goal: evolve the Electron UI into a real experiment workbench.

Planned work:

- Organism editor panel.
- Field editor panel.
- Time slider for snapshots.
- Side-by-side field overlays.
- Experiment save/load.
- Run archive browser.
- Local report viewer.

Exit criteria:

- A non-coder can design, run, inspect, and compare experiments from the UI.

## v0.7 — NexusGate Integration Candidate

Goal: integrate only after standalone behavior is stable.

Planned integration shape:

```text
NexusGate lane -> Petri Dish Pro engine -> artifact bundle -> validation receipt -> Electron card/HUD
```

Boundary:

- NexusGate should govern authority and evidence.
- Petri Dish Pro should own simulation and artifacts.
- Electron should present the organism cockpit.
- No autonomous biological claims, repo mutation, or durable promotion without human authorization.

## v1.0 — Governed Scientific Sandbox

Goal: a clean, local-first biological simulation sandbox with explicit evidence gates.

Required before v1.0:

- Stable organism schema.
- Stable experiment schema.
- Stable artifact schema.
- Validation scorecard.
- Reproducible batch runs.
- UI run archive.
- Clear claim boundary in every export.
- NexusGate-compatible lane contract.

## Non-claim lock

Petri Dish Pro is not a clinical, diagnostic, epidemiological, wet-lab, treatment, or strain-accurate tool. It is a local exploratory simulation platform for learning, architecture, visualization, and future standards integration.
