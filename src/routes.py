import csv
from pathlib import Path

from flask import Flask, Response, redirect, render_template, url_for

from .config import ANNEXES, HYPOTHESES
from .flowchart import create_biochar_flowchart


def load_annex_table(annex_id: str) -> tuple[list[dict], list[str]]:
    """Load and parse an Annex CSV file.

    Args:
        annex_id: The annex identifier (e.g., "II", "III", "IV", etc.)

    Returns:
        Tuple of (rows, cleaned_column_names)
    """
    csv_path = Path(__file__).parent.parent / "annex_data" / f"annex{annex_id}.csv"
    rows = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Get original headers
        original_headers = reader.fieldnames or []
        # Clean headers: remove BOM, non-breaking spaces, etc.
        cleaned_headers = [h.replace("\ufeff", "").replace("\xa0", "").replace("\u202f", "").strip() for h in original_headers]

        # Read rows with cleaned headers
        for row in reader:
            cleaned_row = {}
            for old_key, new_key in zip(original_headers, cleaned_headers, strict=True):
                value = row.get(old_key, "").replace("\xa0", "").replace("\u202f", "").strip()
                cleaned_row[new_key] = value
            rows.append(cleaned_row)

    return rows, cleaned_headers


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
        table_data, column_names = load_annex_table("II")
        return render_template(
            "annex_check.html",
            title="Annex II Check",
            question="Is the Annex II basic checklist complete?",
            yes_url=url_for("select_hypothesis"),
            no_url=url_for("reject"),
            table_data=table_data,
            column_names=column_names,
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

        table_data, column_names = load_annex_table(annex_id)
        return render_template(
            "annex_check.html",
            title=f"Annex {annex_id} Check",
            question=f"Is the Annex {annex_id} checklist complete?",
            yes_url=url_for("proceed_review"),
            no_url=url_for("reject"),
            table_data=table_data,
            column_names=column_names,
        )

    @app.route("/result/reject")
    def reject() -> str:
        return render_template("reject.html")

    @app.route("/result/proceed-review")
    def proceed_review() -> str:
        return render_template("proceed_review.html")
