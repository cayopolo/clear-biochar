# Annex information - maps annex ID to hypothesis and color
ANNEXES = {
    "VII": {"hypothesis": "Soil Biology", "color": "#FFB3BA"},
    "VI": {"hypothesis": "Soil Structure", "color": "#BAFFC9"},
    "V": {"hypothesis": "Soil Remediation", "color": "#BAE1FF"},
    "IV": {"hypothesis": "GHGs", "color": "#FFFFBA"},
    "III": {"hypothesis": "Plant Growth", "color": "#FFD9BA"},
}

# Hypothesis options for selection
HYPOTHESES = [
    {"id": "soil-biology", "label": "Soil Biology", "annex": "VII"},
    {"id": "soil-structure", "label": "Soil Structure", "annex": "VI"},
    {"id": "soil-remediation", "label": "Soil Remediation", "annex": "V"},
    {"id": "ghgs", "label": "GHGs", "annex": "IV"},
    {"id": "plant-growth", "label": "Plant Growth", "annex": "III"},
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
