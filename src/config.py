# Annex information - maps annex ID to hypothesis, color, and title
ANNEXES = {
    "II": {"hypothesis": "Universal", "color": "#E8E8E8", "title": "ANNEX II Universal CLEAR"},
    "III": {"hypothesis": "Soil structure & hydrology", "color": "#FFD9BA", "title": "ANNEX III Soil Structure and Hydrology CLEAR"},
    "IV": {
        "hypothesis": "Soil biodiversity & ecotoxicology",
        "color": "#FFFFBA",
        "title": "ANNEX IV Soil Biodiversity and Ecotoxicology CLEAR",
    },
    "V": {
        "hypothesis": "Soil organic matter & GHGs",
        "color": "#BAE1FF",
        "title": "ANNEX V Soil Organic Matter and Greenhouse Gases CLEAR",
    },
    "VI": {
        "hypothesis": "Nutrient cycling & crop production",
        "color": "#BAFFC9",
        "title": "ANNEX VI Nutrient Cycling and Crop Production CLEAR",
    },
    "VII": {"hypothesis": "Soil remediation", "color": "#FFB3BA", "title": "ANNEX VII Soil Remediation CLEAR"},
}

# Hypothesis options for selection
HYPOTHESES = [
    {"id": "soil-structure", "label": "Soil structure & hydrology", "annex": "III"},
    {"id": "soil-biodiversity", "label": "Soil biodiversity & ecotoxicology", "annex": "IV"},
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
