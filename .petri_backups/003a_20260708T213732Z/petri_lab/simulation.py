from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Any, List, Tuple
import math
import random
import time

from .schemas import ExperimentSpec, OrganismSpec
from .grid import Grid, zeros, clamp, diffuse, total, normalize, downsample, max_value
from .science_notes import CLAIM_BOUNDARY, MODEL_NOTES


def _spot(g: Grid, cx: int, cy: int, radius: float, amount: float) -> None:
    n = len(g)
    r2 = radius * radius
    for y in range(n):
        for x in range(n):
            d2 = (x - cx) * (x - cx) + (y - cy) * (y - cy)
            if d2 <= r2:
                falloff = 1.0 - (d2 / max(r2, 1.0))
                g[y][x] += amount * falloff


def _seed_population(n: int, rng: random.Random, cells: float, organism_index: int, organism_count: int) -> Grid:
    g = zeros(n)
    angle = 2.0 * math.pi * organism_index / max(organism_count, 1)
    ring = n * 0.22
    cx = int(n * 0.5 + math.cos(angle) * ring + rng.uniform(-n * 0.04, n * 0.04))
    cy = int(n * 0.5 + math.sin(angle) * ring + rng.uniform(-n * 0.04, n * 0.04))
    cx = max(3, min(n - 4, cx))
    cy = max(3, min(n - 4, cy))
    radius = max(3.0, n * 0.055)
    _spot(g, cx, cy, radius, cells / (math.pi * radius * radius))
    for _ in range(max(4, int(cells // 4))):
        sx = max(0, min(n - 1, int(rng.gauss(cx, radius * 0.65))))
        sy = max(0, min(n - 1, int(rng.gauss(cy, radius * 0.65))))
        g[sy][sx] += rng.uniform(0.05, 0.24)
    return g


def _initialize_fields(exp: ExperimentSpec, rng: random.Random) -> Dict[str, Grid]:
    n = exp.grid_size
    nutrient = zeros(n, exp.fields.nutrient_level)
    oxygen = zeros(n, exp.fields.oxygen_level)
    toxin = zeros(n, exp.fields.toxin_level)
    waste = zeros(n, exp.fields.waste_level)

    for _ in range(exp.fields.nutrient_hotspots):
        cx = rng.randint(int(n * 0.15), int(n * 0.85))
        cy = rng.randint(int(n * 0.15), int(n * 0.85))
        _spot(nutrient, cx, cy, rng.uniform(n * 0.06, n * 0.14), rng.uniform(0.25, 0.65))

    for _ in range(exp.fields.toxin_spots):
        cx = rng.randint(0, n - 1)
        cy = rng.randint(0, n - 1)
        _spot(toxin, cx, cy, rng.uniform(n * 0.05, n * 0.13), rng.uniform(0.06, 0.16))

    if exp.fields.edge_antibiotic_gradient:
        for y in range(n):
            for x in range(n):
                edge = max(x / max(n - 1, 1), y / max(n - 1, 1))
                toxin[y][x] += 0.13 * edge * edge

    for y in range(n):
        for x in range(n):
            # Oxygen slightly lower in center, higher near edges.
            dx = (x - n / 2) / (n / 2)
            dy = (y - n / 2) / (n / 2)
            radial = min(1.0, math.sqrt(dx * dx + dy * dy))
            oxygen[y][x] = clamp(oxygen[y][x] * (0.70 + 0.30 * radial), 0.0, 1.25)
            nutrient[y][x] = max(0.0, nutrient[y][x])
            toxin[y][x] = max(0.0, toxin[y][x])
            waste[y][x] = max(0.0, waste[y][x])

    return {"nutrient": nutrient, "oxygen": oxygen, "toxin": toxin, "waste": waste}


def _combined_density(populations: Dict[str, Grid]) -> Grid:
    ids = list(populations.keys())
    if not ids:
        return []
    n = len(populations[ids[0]])
    out = zeros(n)
    for g in populations.values():
        for y in range(n):
            row = out[y]
            grow = g[y]
            for x in range(n):
                row[x] += grow[x]
    return out


def run_experiment(exp: ExperimentSpec) -> Dict[str, Any]:
    start = time.time()
    rng = random.Random(exp.seed)
    n = max(16, min(180, int(exp.grid_size)))
    exp.grid_size = n
    steps = max(1, min(2000, int(exp.steps)))
    exp.steps = steps

    fields = _initialize_fields(exp, rng)
    populations: Dict[str, Grid] = {}
    for idx, organism in enumerate(exp.organisms):
        populations[organism.id] = _seed_population(n, rng, organism.initial_cells, idx, len(exp.organisms))

    curves: List[Dict[str, Any]] = []
    snapshots: List[Dict[str, Any]] = []
    organism_map = {o.id: o for o in exp.organisms}

    for step in range(steps + 1):
        if step % max(1, exp.sample_every) == 0:
            rec: Dict[str, Any] = {"step": step}
            for oid, grid in populations.items():
                rec[oid] = round(total(grid), 6)
            rec["total_density"] = round(total(_combined_density(populations)), 6)
            rec["nutrient_total"] = round(total(fields["nutrient"]), 6)
            rec["toxin_total"] = round(total(fields["toxin"]), 6)
            rec["waste_total"] = round(total(fields["waste"]), 6)
            curves.append(rec)

        if step in {0, steps // 3, (2 * steps) // 3, steps}:
            snapshots.append({
                "step": step,
                "density": downsample(normalize(_combined_density(populations)), 72),
            })

        if step >= steps:
            break

        total_density = _combined_density(populations)
        new_populations: Dict[str, Grid] = {}

        # Baseline growth/death/motility update.
        for org in exp.organisms:
            g = populations[org.id]
            moved = diffuse(g, clamp(org.motility * exp.diffusion_rate, 0.0, 0.42))
            out = zeros(n)
            capacity = max(1.0, exp.carrying_capacity * max(0.15, org.carrying_capacity_share))
            for y in range(n):
                for x in range(n):
                    cells = moved[y][x]
                    if cells <= 1e-12:
                        out[y][x] = 0.0
                        continue
                    nutrient = fields["nutrient"][y][x]
                    oxygen = fields["oxygen"][y][x]
                    toxin = fields["toxin"][y][x]
                    waste = fields["waste"][y][x]
                    crowd = clamp(1.0 - (total_density[y][x] / capacity), 0.0, 1.0)
                    nutrient_term = nutrient / (nutrient + max(0.01, org.nutrient_affinity))
                    oxygen_term = 0.65 + 0.35 * (oxygen / (oxygen + max(0.01, org.oxygen_affinity)))
                    effective_toxin = max(0.0, toxin * (1.0 - clamp(org.resistance, 0.0, 0.98)))
                    growth = org.growth_rate * cells * nutrient_term * oxygen_term * crowd
                    stress_death = cells * (org.death_rate + org.toxin_sensitivity * effective_toxin * 0.035 + org.waste_sensitivity * waste * 0.020)
                    next_cells = max(0.0, cells + growth - stress_death)
                    out[y][x] = next_cells
                    fields["nutrient"][y][x] = max(0.0, nutrient - growth * 0.010 - cells * 0.00005)
                    fields["oxygen"][y][x] = clamp(oxygen - growth * 0.0025 + 0.0008, 0.0, 1.25)
                    fields["waste"][y][x] = max(0.0, waste + cells * 0.00016 + stress_death * 0.006)
                    if org.produces_toxin > 0:
                        fields["toxin"][y][x] += org.produces_toxin * cells
            new_populations[org.id] = out

        # Predator-prey / immune-like consumption coupling.
        for org in exp.organisms:
            if not org.consumes_prey or org.id not in new_populations:
                continue
            predator = new_populations[org.id]
            for prey_id in org.prey_ids:
                if prey_id not in new_populations:
                    continue
                prey = new_populations[prey_id]
                for y in range(n):
                    for x in range(n):
                        contact = min(prey[y][x], predator[y][x] * org.predation_rate)
                        if contact > 0:
                            prey[y][x] = max(0.0, prey[y][x] - contact)
                            predator[y][x] += contact * 0.24
                            fields["waste"][y][x] += contact * 0.002

        populations = new_populations
        fields["nutrient"] = diffuse(fields["nutrient"], clamp(exp.nutrient_diffusion, 0.0, 0.35))
        fields["toxin"] = diffuse(fields["toxin"], clamp(exp.toxin_diffusion, 0.0, 0.35))
        fields["waste"] = diffuse(fields["waste"], 0.018)

        # Mild replenishment/decay terms.
        for y in range(n):
            for x in range(n):
                fields["nutrient"][y][x] = clamp(fields["nutrient"][y][x] + 0.00055, 0.0, 2.0)
                fields["toxin"][y][x] = max(0.0, fields["toxin"][y][x] * 0.9975)
                fields["waste"][y][x] = max(0.0, fields["waste"][y][x] * 0.999)

    final_density = _combined_density(populations)
    final_density_norm = normalize(final_density)
    organism_summaries = []
    for org in exp.organisms:
        grid = populations[org.id]
        organism_summaries.append({
            "id": org.id,
            "label": org.label,
            "kind": org.kind,
            "final_population": round(total(grid), 6),
            "max_cell_density": round(max_value(grid), 6),
            "color": org.color,
            "notes": org.notes,
        })

    result = {
        "run_id": f"petri_{int(start)}_{exp.seed}",
        "created_at_epoch": start,
        "runtime_seconds": round(time.time() - start, 6),
        "engine": "petri_spatial_agent_grid_v0_1_stdlib",
        "claim_boundary": CLAIM_BOUNDARY,
        "model_notes": MODEL_NOTES,
        "experiment": exp.to_dict(),
        "organisms": organism_summaries,
        "curves": curves,
        "snapshots": snapshots,
        "density": {
            "size": len(final_density_norm),
            "normalized": downsample(final_density_norm, 96),
            "raw_downsampled": downsample(final_density, 96),
        },
        "fields": {
            "nutrient": downsample(normalize(fields["nutrient"]), 96),
            "toxin": downsample(normalize(fields["toxin"]), 96),
            "oxygen": downsample(normalize(fields["oxygen"]), 96),
            "waste": downsample(normalize(fields["waste"]), 96),
        },
        "metrics": {
            "final_total_population": round(total(final_density), 6),
            "final_max_density": round(max_value(final_density), 6),
            "nutrient_total": round(total(fields["nutrient"]), 6),
            "toxin_total": round(total(fields["toxin"]), 6),
            "waste_total": round(total(fields["waste"]), 6),
            "organism_count": len(exp.organisms),
            "grid_size": n,
            "steps": steps,
            "seed": exp.seed,
        },
    }
    return result
