# Petri Dish Pro — Standalone Scientific Microscope Simulator

Petri Dish Pro is a standalone desktop/web simulation repo for exploratory biological modeling. It combines a Python simulation engine with an Electron microscope cockpit.

It is built as a scientific toy platform: useful for education, prototyping, and model architecture experiments. It is **not** a clinical, diagnostic, wet-lab, epidemiological, or treatment decision tool.

## What it includes

- Pure Python spatial-agent / reaction-field engine.
- Organism presets: fast microbe, spore former, yeast-like colony, predator microbe, antibiotic-resistant variant, immune-like cell, cancer-like clone, infected cell.
- Nutrient, toxin/antibiotic, oxygen, waste, density, and interaction fields.
- Density maps, population curves, run summaries, validation receipts, and reproducible artifacts.
- Electron UI with zoom, pan, microscope canvas, density view, organism controls, experiment presets, and report loading.
- Tests and a first-run demo.
- Organism Gate terminal entrypoint inspired by the NexusGate command surface.
- One-shot PowerShell bootstrap script for Windows.


## Main entrypoint — Organism Gate

Use the organism terminal gate when you want the Nexus-style command entry before opening the Electron HUD:

```powershell
cd PetriDishPro
.\ORGANISM_GATE.ps1
```

Double-click fallback on Windows:

```text
START_ORGANISM_GATE.bat
```

The gate can launch the Electron microscope, run organism presets, open artifacts, print the latest validation receipt, run tests, and show the roadmap.

## Quick start — Python engine only

```powershell
cd PetriDishPro
python -m petri_lab.cli --root . --preset microbial_competition --json
python -m unittest discover -s tests
```

Outputs are written to:

```text
reports/latest_run.json
reports/latest_density.json
reports/latest_summary.md
artifacts/runs/<run_id>/
```

## Quick start — Electron UI

```powershell
cd PetriDishPro
electron\START_ELECTRON.ps1
```

Or manually:

```powershell
cd electron
npm install
npm start
```

The Electron shell calls the Python engine and renders the latest run.

## Windows one-shot setup

```powershell
cd PetriDishPro
.\RUN_DEMO_ALL_ONE.ps1
```

This script checks Python, runs tests, runs a demo simulation, and launches the Electron UI if Node/npm are available.

## Scientific model boundary

This simulator uses simplified grid dynamics:

- Logistic growth constrained by local carrying capacity.
- Nutrient-limited growth using a Monod-like saturation term.
- Diffusive motility through local neighborhood averaging.
- Toxin/antibiotic sensitivity and resistance factors.
- Predator-prey consumption coupling.
- Oxygen and waste fields for cellular/tissue-like experiments.
- Validation checks for finite values, non-negative populations, reproducibility metadata, and claim-boundary receipts.

It does not model real strains, real pharmacokinetics, real immune dynamics, full stochastic chemical kinetics, or validated patient/tissue outcomes.

## Core loop

```text
ExperimentSpec -> Python Simulation -> Artifact Bundle -> Validation Receipt -> Electron Microscope View
```

No artifact is promoted without a validation receipt. No biological claim is elevated beyond the declared boundary.

## Roadmap

See `ROADMAP.md` for the staged evolution plan. Short form:

- v0.2: richer Organism Gate and operator surface.
- v0.3: better biology kernels: interaction matrix, mutation/adaptation, dormancy, chemotaxis, biofilm behavior.
- v0.4: scientific artifact layer: CSV/SVG/PNG exports, sweeps, comparison reports.
- v0.5: dataset and standards adapters: CSV, SBML stubs, AnnData/h5ad design, provenance manifests.
- v0.6: Electron lab workbench: organism editor, field editor, archive browser, time slider.
- v0.7: NexusGate lane candidate after standalone validation.
- v1.0: governed scientific sandbox with stable schemas, validation scorecards, and evidence-bound exports.
