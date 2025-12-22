# Annex information - maps annex ID to hypothesis and color
ANNEXES = {
    "III": {"hypothesis": "Soil structure & hydrology", "color": "#FFD9BA"},
    "IV": {"hypothesis": "Soil biology & ecotoxicology", "color": "#FFFFBA"},
    "V": {"hypothesis": "Soil organic matter & GHGs", "color": "#BAE1FF"},
    "VI": {"hypothesis": "Nutrient cycling & crop production", "color": "#BAFFC9"},
    "VII": {"hypothesis": "Soil remediation", "color": "#FFB3BA"},
}

# Hypothesis options for selection
HYPOTHESES = [
    {"id": "soil-structure", "label": "Soil structure & hydrology", "annex": "III"},
    {"id": "soil-biodiversity", "label": "Soil biology & ecotoxicology", "annex": "IV"},
    {"id": "ghgs", "label": "Soil organic matter & GHGs", "annex": "V"},
    {"id": "plant-growth", "label": "Nutrient cycling & crop production", "annex": "VI"},
    {"id": "soil-remediation", "label": "Soil remediation", "annex": "VII"},
]

# Workflow steps for progress tracking
WORKFLOW_STEPS = [
    {"id": "topic-check", "label": "Topic Check", "order": 1},
    {"id": "annex-ii-check", "label": "Annex II", "order": 2},
    {"id": "select-hypothesis", "label": "Hypothesis", "order": 3},
    {"id": "apply-annex", "label": "Apply Annex", "order": 4},
    {"id": "verify-annex", "label": "Verification", "order": 5},
    {"id": "summary", "label": "Summary", "order": 6},
]


def get_step_by_id(step_id: str) -> dict | None:
    """Get a workflow step by its ID."""
    for step in WORKFLOW_STEPS:
        if step["id"] == step_id:
            return step
    return None


def get_previous_step(current_step_id: str) -> dict | None:
    """Get the previous step in the workflow."""
    current = get_step_by_id(current_step_id)
    if not current or current["order"] <= 1:
        return None
    for step in WORKFLOW_STEPS:
        if step["order"] == current["order"] - 1:
            return step
    return None
