from flask import Flask, Response, redirect, render_template, url_for

from .config import ANNEXES, HYPOTHESES
from .flowchart import create_biochar_flowchart


def init_app(app: Flask) -> None:
    """Register all routes on the Flask app."""

    @app.route("/")
    def home() -> str:
        flowchart_svg = create_biochar_flowchart()
        return render_template("home.html", flowchart_svg=flowchart_svg)

    @app.route("/start")
    def start_workflow() -> Response:
        return redirect(url_for("topic_check"))

    @app.route("/step/topic-check")
    def topic_check() -> str:
        return render_template(
            "binary_question.html",
            title="Topic Check",
            question="Is the MA topic on biochar application to soils?",
            yes_url=url_for("annex_ii_check"),
            no_url=url_for("reject"),
        )

    @app.route("/step/annex-ii-check")
    def annex_ii_check() -> str:
        return render_template(
            "binary_question.html",
            title="Annex II Check",
            question="Is the Annex II basic checklist complete?",
            yes_url=url_for("select_hypothesis"),
            no_url=url_for("reject"),
        )

    @app.route("/step/select-hypothesis")
    def select_hypothesis() -> str:
        colors = {annex_id: data["color"] for annex_id, data in ANNEXES.items()}
        return render_template("hypothesis.html", hypotheses=HYPOTHESES, colors=colors)

    @app.route("/step/apply-annex/<annex_id>")
    def apply_annex(annex_id: str) -> str | Response:
        if annex_id not in ANNEXES:
            return redirect(url_for("home"))

        annex_info = ANNEXES[annex_id]
        return render_template("annex.html", annex_id=annex_id, hypothesis=annex_info["hypothesis"], color=annex_info["color"])

    @app.route("/step/check-annex/<annex_id>")
    def check_annex(annex_id: str) -> str | Response:
        if annex_id not in ANNEXES:
            return redirect(url_for("home"))

        return render_template(
            "binary_question.html",
            title=f"Annex {annex_id} Check",
            question=f"Is the Annex {annex_id} checklist complete?",
            yes_url=url_for("proceed_review"),
            no_url=url_for("reject"),
        )

    @app.route("/result/reject")
    def reject() -> str:
        return render_template("reject.html")

    @app.route("/result/proceed-review")
    def proceed_review() -> str:
        return render_template("proceed_review.html")
