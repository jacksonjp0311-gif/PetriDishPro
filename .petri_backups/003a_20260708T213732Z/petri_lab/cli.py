from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .schemas import ExperimentSpec
from .presets import PRESETS
from .simulation import run_experiment
from .artifacts import write_artifact_bundle


def load_experiment(path: Path) -> ExperimentSpec:
    data = json.loads(path.read_text(encoding="utf-8"))
    return ExperimentSpec.from_dict(data)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run Petri Dish Pro simulations.")
    parser.add_argument("--root", default=".", help="Repo/output root.")
    parser.add_argument("--preset", default="microbial_competition", choices=sorted(PRESETS.keys()))
    parser.add_argument("--experiment", default="", help="Optional experiment JSON path.")
    parser.add_argument("--grid", type=int, default=0, help="Override grid size.")
    parser.add_argument("--steps", type=int, default=0, help="Override step count.")
    parser.add_argument("--seed", type=int, default=None, help="Override seed.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result pointer.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=True)

    if args.experiment:
        exp = load_experiment(Path(args.experiment))
    else:
        exp = PRESETS[args.preset]()

    if args.grid > 0:
        exp.grid_size = args.grid
    if args.steps > 0:
        exp.steps = args.steps
    if args.seed is not None:
        exp.seed = args.seed

    result = run_experiment(exp)
    bundle = write_artifact_bundle(root, result)

    payload = {
        "ok": bundle.get("status") == "pass",
        "run_id": result.get("run_id"),
        "preset": exp.preset,
        "paths": bundle,
        "metrics": result.get("metrics", {}),
        "claim_boundary": result.get("claim_boundary"),
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Petri Dish Pro run complete: {result.get('run_id')}")
        print(f"Validation: {bundle.get('status')}")
        print(f"Latest report: {bundle.get('latest_summary')}")
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
