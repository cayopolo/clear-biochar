import csv
from pathlib import Path

from flask import Flask, Response, redirect, render_template, session, url_for

from .config import ANNEXES, HYPOTHESES, WORKFLOW_STEPS, get_previous_step, get_step_by_id
from .flowchart import create_biochar_flowchart


def init_session() -> None:
    """Initialize or reset the workflow session."""
    session["current_step"] = None
    session["hypothesis"] = None
    session["annex_id"] = None
    session["answers"] = {}
    session["rejection_reason"] = None


def update_session_step(step_id: str) -> None:
    """Update the current step in the session."""
    session["current_step"] = step_id


def record_answer(step_id: str, *, passed: bool) -> None:
    """Record a user's answer for a step."""
    if "answers" not in session:
        session["answers"] = {}
    session["answers"][step_id] = passed
    session.modified = True


def get_step_context(step_id: str) -> dict:
    """Get the context needed for rendering the progress stepper."""
    current_step = get_step_by_id(step_id)
    prev_step = get_previous_step(step_id)

    # Build previous URL based on the previous step
    prev_url = None
    if prev_step:
        step_url_map = {
            "topic-check": "topic_check",
            "annex-ii-check": "annex_ii_check",
            "select-hypothesis": "select_hypothesis",
            "apply-annex": "apply_annex",
            "verify-annex": "check_annex",
        }
        route_name = step_url_map.get(prev_step["id"])
        if route_name:
            annex_id = session.get("annex_id")
            if route_name in ("apply_annex", "check_annex") and annex_id:
                prev_url = url_for(route_name, annex_id=annex_id)
            elif route_name in ("apply_annex", "check_annex"):
                # No annex_id in session yet, skip prev link
                prev_url = None
            else:
                prev_url = url_for(route_name)

    return {"steps": WORKFLOW_STEPS, "current_step": current_step, "prev_url": prev_url}


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
                value = row.get(old_key) or ""
                value = value.replace("\xa0", "").replace("\u202f", "").strip()
                cleaned_row[new_key] = value
            rows.append(cleaned_row)

    return rows, cleaned_headers


def init_app(app: Flask) -> None:
    """Register all routes on the Flask app."""

    @app.route("/")
    def home() -> str:
        flowchart_svg = create_biochar_flowchart()
        return render_template("home.html", flowchart_svg=flowchart_svg, show_nav=False)

    @app.route("/start")
    def start_workflow() -> Response:
        init_session()
        return redirect(url_for("topic_check"))

    @app.route("/step/topic-check")
    def topic_check() -> str:
        update_session_step("topic-check")
        step_context = get_step_context("topic-check")
        return render_template(
            "binary_question.html",
            title="Topic Check - Biochar MA Review",
            question="Is the MA topic on biochar application to soils?",
            yes_url=url_for("record_yes", step="topic-check", next_route="annex_ii_check"),
            no_url=url_for("confirm_reject", from_step="topic-check"),
            **step_context,
        )

    @app.route("/step/annex-ii-check")
    def annex_ii_check() -> str:
        update_session_step("annex-ii-check")
        step_context = get_step_context("annex-ii-check")
        table_data, column_names = load_annex_table("II")
        return render_template(
            "annex_check.html",
            title=ANNEXES["II"]["title"],
            question="Is the Annex II basic checklist complete?",
            yes_url=url_for("record_yes", step="annex-ii-check", next_route="select_hypothesis"),
            no_url=url_for("confirm_reject", from_step="annex-ii-check"),
            table_data=table_data,
            column_names=column_names,
            instructions="Review each item in the checklist below. All basic criteria must be met before proceeding.",
            **step_context,
        )

    @app.route("/step/select-hypothesis")
    def select_hypothesis() -> str:
        update_session_step("select-hypothesis")
        step_context = get_step_context("select-hypothesis")
        colors = {annex_id: data["color"] for annex_id, data in ANNEXES.items()}
        return render_template(
            "hypothesis.html", title="Select Hypothesis - Biochar MA Review", hypotheses=HYPOTHESES, colors=colors, **step_context
        )

    @app.route("/step/apply-annex/<annex_id>")
    def apply_annex(annex_id: str) -> str | Response:
        if annex_id not in ANNEXES:
            return redirect(url_for("home"))

        update_session_step("apply-annex")
        session["annex_id"] = annex_id
        session["hypothesis"] = ANNEXES[annex_id]["hypothesis"]
        step_context = get_step_context("apply-annex")
        annex_info = ANNEXES[annex_id]
        return render_template(
            "annex.html",
            title=annex_info["title"],
            annex_id=annex_id,
            hypothesis=annex_info["hypothesis"],
            color=annex_info["color"],
            **step_context,
        )

    @app.route("/step/check-annex/<annex_id>")
    def check_annex(annex_id: str) -> str | Response:
        if annex_id not in ANNEXES:
            return redirect(url_for("home"))

        update_session_step("verify-annex")
        step_context = get_step_context("verify-annex")
        table_data, column_names = load_annex_table(annex_id)
        return render_template(
            "annex_check.html",
            title=ANNEXES[annex_id]["title"],
            question=f"Is the Annex {annex_id} checklist complete?",
            yes_url=url_for("record_yes", step="verify-annex", next_route="summary"),
            no_url=url_for("confirm_reject", from_step="verify-annex"),
            table_data=table_data,
            column_names=column_names,
            instructions=(
                f"Review each item in the Annex {annex_id} checklist for "
                f"{ANNEXES[annex_id]['hypothesis']}. Ensure all criteria are addressed."
            ),
            **step_context,
        )

    @app.route("/action/record-yes")
    def record_yes() -> Response:
        """Record a 'Yes' answer and redirect to the next route."""
        from flask import request

        step = request.args.get("step")
        next_route = request.args.get("next_route")

        if step:
            record_answer(step, passed=True)

        return redirect(url_for(next_route))

    @app.route("/confirm/reject")
    def confirm_reject() -> str:
        """Show confirmation page before rejecting."""
        from flask import request

        from_step = request.args.get("from_step", "unknown")
        step_labels = {
            "topic-check": "Topic Check",
            "annex-ii-check": "Annex II Checklist",
            "verify-annex": f"Annex {session.get('annex_id', '')} Verification",
        }
        step_label = step_labels.get(from_step, from_step)

        # Build go back URL
        annex_id = session.get("annex_id") or "II"
        back_url_map = {
            "topic-check": url_for("topic_check"),
            "annex-ii-check": url_for("annex_ii_check"),
            "verify-annex": url_for("check_annex", annex_id=annex_id),
        }
        back_url = back_url_map.get(from_step, url_for("home"))

        return render_template(
            "confirm_action.html",
            title="Confirm Rejection - Biochar MA Review",
            action_type="reject",
            step_label=step_label,
            from_step=from_step,
            back_url=back_url,
            confirm_url=url_for("do_reject", from_step=from_step),
            show_nav=False,
        )

    @app.route("/action/do-reject")
    def do_reject() -> Response:
        """Actually perform the rejection after confirmation."""
        from flask import request

        from_step = request.args.get("from_step", "unknown")
        record_answer(from_step, passed=False)
        session["rejection_reason"] = from_step
        return redirect(url_for("reject"))

    @app.route("/step/summary")
    def summary() -> str:
        """Show summary of all answers before final approval."""
        update_session_step("summary")
        step_context = get_step_context("summary")

        answers = session.get("answers", {})
        hypothesis = session.get("hypothesis", "Not selected")
        annex_id = session.get("annex_id", "")

        summary_items = []
        if answers.get("topic-check"):
            summary_items.append({"label": "Topic Check", "value": "Biochar application to soils", "passed": True})
        if answers.get("annex-ii-check"):
            summary_items.append({"label": "Annex II Checklist", "value": "Complete", "passed": True})
        if hypothesis != "Not selected":
            summary_items.append({"label": "Selected Hypothesis", "value": hypothesis, "passed": True})
        if answers.get("verify-annex"):
            summary_items.append({"label": f"Annex {annex_id} Verification", "value": "Complete", "passed": True})

        return render_template(
            "summary.html",
            title="Review Summary - Biochar MA Review",
            summary_items=summary_items,
            hypothesis=hypothesis,
            annex_id=annex_id,
            **step_context,
        )

    @app.route("/result/reject")
    def reject() -> str:
        rejection_reason = session.get("rejection_reason", "unknown")
        annex_id = session.get("annex_id", "")
        hypothesis = session.get("hypothesis", "the selected hypothesis")
        reason_messages = {
            "topic-check": "The meta-analysis topic is not about biochar application to soils.",
            "annex-ii-check": "The Annex II basic checklist requirements were not met.",
            "verify-annex": f"The Annex {annex_id} checklist for {hypothesis} was not complete.",
        }
        reason_message = reason_messages.get(rejection_reason, "The submission did not meet the required criteria.")

        return render_template(
            "reject.html", title="Submission Rejected - Biochar MA Review", reason_message=reason_message, show_nav=False
        )

    @app.route("/result/proceed-review")
    def proceed_review() -> str:
        hypothesis = session.get("hypothesis", "the selected hypothesis")
        annex_id = session.get("annex_id", "")

        return render_template(
            "proceed_review.html", title="Approved - Biochar MA Review", hypothesis=hypothesis, annex_id=annex_id, show_nav=False
        )
