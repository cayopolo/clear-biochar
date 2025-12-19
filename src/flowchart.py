import graphviz

from .config import ANNEXES


def create_biochar_flowchart() -> str:
    """Create a Graphviz flowchart showing the biochar MA review workflow"""
    dot = graphviz.Digraph(comment="Biochar MA Review Workflow", format="svg")

    dot.attr(rankdir="TD", bgcolor="white", splines="ortho")
    dot.attr("node", style="filled", fontname="Arial", fontsize="10")
    dot.attr("edge", fontsize="9")

    # Start node
    dot.node("start", "Is the MA topic on\\nbiochar application\\nto soils?", shape="box", fillcolor="lightblue")

    # Decision nodes
    dot.node("checkannex2", "Annex II basic\\nchecklist is\\ncomplete", shape="diamond", fillcolor="lightyellow")
    dot.node("reject", "Reject", shape="box", fillcolor="lightcoral")
    dot.node("proceedreview", "Proceed review", shape="box", fillcolor="lightgreen")

    # Hypothesis selection
    dot.node("selecthyp", "Select\\nmain\\nhypothesis", shape="circle", fillcolor="lightgray")

    # Hypothesis nodes
    dot.node("soilbio", "Soil biology", shape="diamond", fillcolor=ANNEXES["VII"]["color"])
    dot.node("soilstruct", "Soil structure", shape="diamond", fillcolor=ANNEXES["VI"]["color"])
    dot.node("soilremed", "Soil\\nremediation", shape="diamond", fillcolor=ANNEXES["V"]["color"])
    dot.node("ghgs", "GHGs", shape="diamond", fillcolor=ANNEXES["IV"]["color"])
    dot.node("plantgrowth", "Plant growth", shape="diamond", fillcolor=ANNEXES["III"]["color"])

    # Apply annex nodes
    dot.node("applyvii", "Apply checklist\\nin Annex VII", shape="box", fillcolor=ANNEXES["VII"]["color"])
    dot.node("applyvi", "Apply checklist\\nin Annex VI", shape="box", fillcolor=ANNEXES["VI"]["color"])
    dot.node("applyv", "Apply checklist\\nin Annex V", shape="box", fillcolor=ANNEXES["V"]["color"])
    dot.node("applyiv", "Apply checklist\\nin Annex IV", shape="box", fillcolor=ANNEXES["IV"]["color"])
    dot.node("applyiii", "Apply checklist\\nin Annex III", shape="box", fillcolor=ANNEXES["III"]["color"])

    # Check annex nodes
    dot.node("checkvii", "Annex VII\\nchecklist is\\ncomplete", shape="diamond", fillcolor=ANNEXES["VII"]["color"])
    dot.node("checkvi", "Annex VI\\nchecklist is\\ncomplete", shape="diamond", fillcolor=ANNEXES["VI"]["color"])
    dot.node("checkv", "Annex V\\nchecklist is\\ncomplete", shape="diamond", fillcolor=ANNEXES["V"]["color"])
    dot.node("checkiv", "Annex IV\\nchecklist is\\ncomplete", shape="diamond", fillcolor=ANNEXES["IV"]["color"])
    dot.node("checkiii", "Annex III\\nchecklist is\\ncomplete", shape="diamond", fillcolor=ANNEXES["III"]["color"])

    # Main flow edges
    dot.edge("start", "checkannex2", label="True")
    dot.edge("start", "reject", label="False")
    dot.edge("checkannex2", "selecthyp", label="True")
    dot.edge("checkannex2", "reject", label="False")

    # Hypothesis selection edges
    dot.edge("selecthyp", "soilbio")
    dot.edge("selecthyp", "soilstruct")
    dot.edge("selecthyp", "soilremed")
    dot.edge("selecthyp", "ghgs")
    dot.edge("selecthyp", "plantgrowth")

    # Hypothesis to apply annex
    dot.edge("soilbio", "applyvii")
    dot.edge("soilstruct", "applyvi")
    dot.edge("soilremed", "applyv")
    dot.edge("ghgs", "applyiv")
    dot.edge("plantgrowth", "applyiii")

    # Apply to check annex
    dot.edge("applyvii", "checkvii")
    dot.edge("applyvi", "checkvi")
    dot.edge("applyv", "checkv")
    dot.edge("applyiv", "checkiv")
    dot.edge("applyiii", "checkiii")

    # Check annex results
    dot.edge("checkvii", "proceedreview", label="True")
    dot.edge("checkvii", "reject", label="False")
    dot.edge("checkvi", "proceedreview", label="True")
    dot.edge("checkvi", "reject", label="False")
    dot.edge("checkv", "proceedreview", label="True")
    dot.edge("checkv", "reject", label="False")
    dot.edge("checkiv", "proceedreview", label="True")
    dot.edge("checkiv", "reject", label="False")
    dot.edge("checkiii", "proceedreview", label="True")
    dot.edge("checkiii", "reject", label="False")

    # Reject loop
    dot.edge("reject", "start", style="dashed", color="gray")

    return dot.pipe(encoding="utf-8")
