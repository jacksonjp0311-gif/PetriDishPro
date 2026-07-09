# Project Structure

## Top-level directory snapshot

- `.petri_backups/`
- `artifacts/`
- `assets/`
- `backups/`
- `config/`
- `docs/`
- `electron/`
- `examples/`
- `petri_lab/`
- `reports/`
- `tests/`
- `tools/`
- `BUILD_FROM_EMPTY_ALL_ONE.ps1`
- `CLAIM_BOUNDARY.md`
- `ORGANISM_GATE.ps1`
- `ORGANISM_GATE_CORE_004O.ps1`
- `pyproject.toml`
- `README.md`
- `requirements.txt`
- `ROADMAP.md`
- `RUN_DEMO_ALL_ONE.ps1`
- `RUN_TESTS_DIGEST.ps1`
- `START_ORGANISM_GATE.bat`

## Common directories

| Path | Role |
| --- | --- |
| `electron/` | Electron application shell and renderer surfaces. |
| `electron/renderer/` | HUD scripts, styles, overlay repairs, and UI behavior layers. |
| `config/` | Organism, preset, field, metric, and drug-card configuration surfaces. |
| `docs/` | Project documentation, entrypoint notes, capability docs, update notes, and assets. |
| `reports/` | Generated run reports, validation digests, and machine-state receipts. |
| `tests/` | Python validation tests and static contract checks. |
| `_backup/` | Local patch backups. This should stay out of Git history. |

## Publication guidance

Keep source, docs, and configuration files in Git. Keep local backups, generated logs, dependency folders, and private environment files out of Git.
