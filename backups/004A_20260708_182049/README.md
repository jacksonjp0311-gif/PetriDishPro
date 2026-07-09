# Petri Dish Pro

Standalone organism simulation lab with a Python simulation core and an Electron microscope HUD.

## Start

```powershell
cd C:\Users\jacks\OneDrive\Desktop\PetriDishPro
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ORGANISM_GATE.ps1
```

Double-click: `START_ORGANISM_GATE.bat`

## Direct Python

```powershell
python -m petri_lab.cli --root . --preset microbial_competition --steps 90 --grid 56 --json
```

## Electron

```powershell
cd electron
npm install
npm start
```

## Receipts

- `reports/bio/petri_run_latest.json`
- `reports/bio/petri_density_latest.json`
- `reports/bio/petri_summary_latest.md`
- `artifacts/bio/runs/<run_id>/`

## Boundary

Educational and research simulation only. Not clinical, diagnostic, wet-lab, treatment, biosafety, or regulatory evidence.

<!-- PETRI_003C_ENTRYPOINT -->

## Organism Gate Entry Point

Petri Dish Pro now has a Windows desktop launcher icon and a repo-local gate script.

Run directly:

```powershell
cd "$env:USERPROFILE\OneDrive\Desktop\PetriDishPro"
powershell -NoProfile -ExecutionPolicy Bypass -File .\ORGANISM_GATE.ps1
```

Double-click fallback:

```text
START_ORGANISM_GATE.bat
```

The gate runs simulations, opens the Electron microscope HUD when dependencies are installed, opens artifact folders, and shows validation receipts.

Claim boundary: educational/research simulation only; not diagnostic, clinical, wet-lab, or safety proof.
