from __future__ import annotations

from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for

from admin_portal import register_admin_routes
from config import Config
from repository import PortalRepository, VECTOR_DIMENSIONS

INCIDENT_CATEGORIES = [
    "Illegal dumping",
    "Air pollution",
    "Water contamination",
    "Flood risk",
    "Disaster response",
    "Wetland encroachment",
    "Wildfire",
    "Noise complaint",
]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    repository = PortalRepository(app.config["SQL_SERVER_CONNECTION"])
    register_admin_routes(app, repository)

    @app.template_filter("date_label")
    def date_label(value: Any, fmt: str = "%d %b %Y") -> str:
        return value.strftime(fmt) if value else ""

    @app.route("/")
    def home() -> str:
        try:
            context = repository.get_home_context()
            return render_template("home.html", db_error=None, **context)
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template("home.html", db_error=database_error_message(exc), **empty_home_context())

    @app.route("/counties")
    def counties() -> str:
        search_term = request.args.get("q", "").strip()
        try:
            county_rows = repository.get_counties(search_term or None)
            return render_template(
                "counties.html",
                counties=county_rows,
                search_term=search_term,
                db_error=None,
            )
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "counties.html",
                counties=[],
                search_term=search_term,
                db_error=database_error_message(exc),
            )

    @app.route("/counties/<int:county_id>")
    def county_details(county_id: int) -> str:
        try:
            county = repository.get_county_details(county_id)
            if county is None:
                return render_template("county_details.html", county=None, db_error=None), 404
            return render_template("county_details.html", county=county, db_error=None)
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "county_details.html",
                county=None,
                db_error=database_error_message(exc),
            )

    @app.route("/licensing")
    def licensing() -> str:
        search_term = normalize_inline_text(request.args.get("q", ""))
        try:
            license_rows = repository.get_licensing_services(search_term or None)
            return render_template(
                "licensing.html",
                licenses=license_rows,
                search_term=search_term,
                db_error=None,
            )
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "licensing.html",
                licenses=[],
                search_term=search_term,
                db_error=database_error_message(exc),
            )

    @app.route("/licensing/apply", methods=["GET", "POST"])
    def license_application() -> str:
        form_data = {
            "applicant_name": normalize_inline_text(request.form.get("applicant_name", "")),
            "applicant_email": normalize_email(request.form.get("applicant_email", "")),
            "organization_name": normalize_inline_text(request.form.get("organization_name", "")),
            "license_service_id": normalize_inline_text(request.form.get("license_service_id", "")),
            "project_county_id": normalize_inline_text(request.form.get("project_county_id", "")),
            "project_location": normalize_inline_text(request.form.get("project_location", "")),
            "project_summary": normalize_block_text(request.form.get("project_summary", "")),
            "supporting_documents": normalize_block_text(
                request.form.get("supporting_documents", "")
            ),
        }

        try:
            context = repository.get_license_application_context()
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "license_application.html",
                license_services=[],
                counties=[],
                recent_applications=[],
                form_data=form_data,
                errors=[],
                db_error=database_error_message(exc),
            )

        if request.method == "POST":
            errors = validate_license_application_form(form_data)
            if errors:
                return render_template(
                    "license_application.html",
                    form_data=form_data,
                    errors=errors,
                    db_error=None,
                    **context,
                )

            try:
                form_data["license_service_id"] = int(form_data["license_service_id"])
                form_data["project_county_id"] = (
                    int(form_data["project_county_id"])
                    if form_data["project_county_id"]
                    else None
                )
                application_id = repository.create_license_application(form_data)
                flash(
                    f"Licence application #{application_id} was submitted successfully.",
                    "success",
                )
                return redirect(url_for("license_application"))
            except Exception as exc:  # pragma: no cover - graceful runtime path
                return render_template(
                    "license_application.html",
                    form_data=form_data,
                    errors=[],
                    db_error=database_error_message(exc),
                    **context,
                )

        return render_template(
            "license_application.html",
            form_data=form_data,
            errors=[],
            db_error=None,
            **context,
        )

    @app.route("/research")
    def research() -> str:
        search_term = normalize_inline_text(request.args.get("q", ""))
        try:
            research_rows = repository.get_research_activities(search_term or None)
            return render_template(
                "research.html",
                research_activities=research_rows,
                search_term=search_term,
                db_error=None,
            )
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "research.html",
                research_activities=[],
                search_term=search_term,
                db_error=database_error_message(exc),
            )

    @app.route("/knowledge-search", methods=["GET", "POST"])
    def knowledge_search() -> str:
        query_text = normalize_inline_text(request.args.get("q", ""))

        try:
            if request.method == "POST":
                rebuild_summary = repository.rebuild_knowledge_index()
                flash(
                    "Search records refreshed: "
                    f"{rebuild_summary['document_count']} documents and "
                    f"{rebuild_summary['index_row_count']} indexed values updated.",
                    "success",
                )
                return redirect(url_for("knowledge_search"))

            summary = repository.get_knowledge_index_summary()
            results = (
                repository.query_knowledge_similarity(query_text)
                if query_text and summary["document_count"] > 0
                else []
            )
            search_hint = (
                "Search information is not available yet. Please refresh the records and try again."
                if query_text and summary["document_count"] == 0
                else None
            )
            return render_template(
                "knowledge_search.html",
                query_text=query_text,
                results=results,
                summary=summary,
                search_hint=search_hint,
                vector_dimensions=VECTOR_DIMENSIONS,
                db_error=None,
            )
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "knowledge_search.html",
                query_text=query_text,
                results=[],
                summary=empty_knowledge_summary(),
                search_hint=None,
                vector_dimensions=VECTOR_DIMENSIONS,
                db_error=database_error_message(exc),
            )

    @app.route("/incident-desk", methods=["GET", "POST"])
    def incident_desk() -> str:
        form_data = {
            "reporter_name": normalize_inline_text(request.form.get("reporter_name", "")),
            "reporter_email": normalize_email(request.form.get("reporter_email", "")),
            "response_location_id": normalize_inline_text(request.form.get("response_location_id", "")),
            "category": normalize_inline_text(request.form.get("category", "")),
            "location": normalize_inline_text(request.form.get("location", "")),
            "description": normalize_block_text(request.form.get("description", "")),
        }

        try:
            response_locations = repository.get_response_locations()
        except Exception as exc:  # pragma: no cover - graceful runtime path
            return render_template(
                "incident_desk.html",
                categories=INCIDENT_CATEGORIES,
                response_locations=[],
                form_data=form_data,
                errors=[],
                db_error=database_error_message(exc),
            )

        if request.method == "POST":
            errors = validate_incident_form(form_data)
            if errors:
                return render_template(
                    "incident_desk.html",
                    categories=INCIDENT_CATEGORIES,
                    response_locations=response_locations,
                    form_data=form_data,
                    errors=errors,
                    db_error=None,
                )

            try:
                form_data["response_location_id"] = int(form_data["response_location_id"])
                report_id = repository.create_incident_report(form_data)
                flash(f"Incident report #{report_id} was submitted successfully.", "success")
                return redirect(url_for("incident_desk"))
            except Exception as exc:  # pragma: no cover - graceful runtime path
                return render_template(
                    "incident_desk.html",
                    categories=INCIDENT_CATEGORIES,
                    response_locations=response_locations,
                    form_data=form_data,
                    errors=[],
                    db_error=database_error_message(exc),
                )

        return render_template(
            "incident_desk.html",
            categories=INCIDENT_CATEGORIES,
            response_locations=response_locations,
            form_data=form_data,
            errors=[],
            db_error=None,
        )

    @app.route("/database")
    def database_guide() -> str:
        return render_template("database.html")

    return app


def empty_home_context() -> dict[str, Any]:
    return {
        "county_count": 47,
        "response_location_count": 48,
        "license_count": 0,
        "research_activity_count": 0,
        "license_application_count": 0,
        "knowledge_document_count": 0,
        "knowledge_index_row_count": 0,
        "program_count": 0,
        "incident_count": 0,
        "quick_services": [],
        "featured_updates": [],
        "latest_updates": [],
        "featured_programs": [],
        "license_highlights": [],
        "research_highlights": [],
        "recent_license_applications": [],
        "knowledge_index_summary": empty_knowledge_summary(),
        "county_highlights": [],
    }


def validate_incident_form(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []

    if not form_data["reporter_name"]:
        errors.append("Full name is required.")
    if not form_data["reporter_email"] or "@" not in form_data["reporter_email"]:
        errors.append("A valid email address is required.")
    if not form_data["response_location_id"]:
        errors.append("Choose a handling office or response location.")
    if not form_data["category"]:
        errors.append("Choose an incident category.")
    if not form_data["location"]:
        errors.append("Incident place or landmark is required.")
    if len(form_data["description"]) < 20:
        errors.append("Description must be at least 20 characters long.")

    return errors


def validate_license_application_form(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []

    if not form_data["applicant_name"]:
        errors.append("Applicant name is required.")
    if not form_data["applicant_email"] or "@" not in form_data["applicant_email"]:
        errors.append("A valid applicant email is required.")
    if not form_data["license_service_id"]:
        errors.append("Choose a licence service.")
    if not form_data["project_location"]:
        errors.append("Project location is required.")
    if len(form_data["project_summary"]) < 30:
        errors.append("Project summary must be at least 30 characters long.")
    if len(form_data["supporting_documents"]) < 12:
        errors.append("List the supporting documents or evidence you will attach.")

    return errors


def empty_knowledge_summary() -> dict[str, Any]:
    return {
        "document_count": 0,
        "index_row_count": 0,
        "last_indexed_at": None,
        "dimension_count": VECTOR_DIMENSIONS,
    }


def normalize_inline_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_block_text(value: str) -> str:
    return " ".join(value.split())


def normalize_email(value: str) -> str:
    return normalize_inline_text(value).lower()


def database_error_message(exc: Exception) -> str:
    return "This service is temporarily unavailable. Please try again later."


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
