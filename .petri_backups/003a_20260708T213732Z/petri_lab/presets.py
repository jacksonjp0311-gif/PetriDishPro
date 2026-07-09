from __future__ import annotations

from .schemas import ExperimentSpec, FieldSpec
from .organisms import (
    ecoli_like,
    bacillus_like,
    yeast_like,
    predator_microbe,
    resistant_variant,
    immune_like_cell,
    cancer_like_cell,
    infected_cell,
)


def microbial_competition() -> ExperimentSpec:
    return ExperimentSpec(
        id="microbial_competition_v0_1",
        name="Microbial Competition Plate",
        description="Fast microbe, spore former, yeast-like colony, predator, and resistant variant compete under nutrient and antibiotic gradients.",
        preset="microbial_competition",
        grid_size=76,
        steps=220,
        sample_every=1,
        seed=20260709,
        carrying_capacity=30.0,
        diffusion_rate=0.075,
        nutrient_diffusion=0.035,
        toxin_diffusion=0.028,
        organisms=[ecoli_like(), bacillus_like(), yeast_like(), predator_microbe(), resistant_variant()],
        fields=FieldSpec(
            nutrient_level=1.0,
            oxygen_level=0.9,
            toxin_level=0.04,
            waste_level=0.0,
            nutrient_hotspots=5,
            toxin_spots=2,
            edge_antibiotic_gradient=True,
        ),
        metadata={"claim_level": "educational_exploratory", "engine": "spatial_agent_grid_v0_1"},
    )


def cellular_tissue() -> ExperimentSpec:
    return ExperimentSpec(
        id="cellular_tissue_v0_1",
        name="Cellular Tissue Interaction",
        description="Cancer-like, immune-like, and infected-cell presets interact across oxygen and waste fields.",
        preset="cellular_tissue",
        grid_size=72,
        steps=200,
        sample_every=1,
        seed=424242,
        carrying_capacity=24.0,
        diffusion_rate=0.060,
        nutrient_diffusion=0.025,
        toxin_diffusion=0.018,
        organisms=[cancer_like_cell(), immune_like_cell(), infected_cell()],
        fields=FieldSpec(
            nutrient_level=0.88,
            oxygen_level=0.65,
            toxin_level=0.02,
            waste_level=0.04,
            nutrient_hotspots=3,
            toxin_spots=1,
            edge_antibiotic_gradient=False,
        ),
        metadata={"claim_level": "educational_exploratory", "engine": "spatial_agent_grid_v0_1"},
    )


def antibiotic_selection() -> ExperimentSpec:
    exp = microbial_competition()
    exp.id = "antibiotic_selection_v0_1"
    exp.name = "Antibiotic Selection Gradient"
    exp.description = "Fast susceptible microbe and resistant variant under stronger edge antibiotic gradient."
    exp.preset = "antibiotic_selection"
    exp.organisms = [ecoli_like(), resistant_variant(), bacillus_like()]
    exp.fields.toxin_level = 0.08
    exp.fields.toxin_spots = 3
    exp.seed = 777
    return exp


PRESETS = {
    "microbial_competition": microbial_competition,
    "cellular_tissue": cellular_tissue,
    "antibiotic_selection": antibiotic_selection,
}
