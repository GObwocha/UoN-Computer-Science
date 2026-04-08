from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from flask import Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from repository import PortalRepository

UPDATE_CATEGORIES = [
    "Alert",
    "Guidance",
    "Press release",
    "News",
    "Project update",
    "Consultation",
    "Research",
]

PROGRAM_STATUSES = [
    "Active",
    "Planned",
    "Monitoring",
    "Completed",
]

INCIDENT_STATUSES = [
    "New",
    "Under review",
    "Escalated",
    "Closed",
]

APPLICATION_STATUSES = [
    "Submitted",
    "Under review",
    "Approved",
    "Rejected",
]

RESEARCH_STATUSES = [
    "Scheduled",
    "Active",
    "Field analysis",
    "Monitoring",
    "Published",
    "Closed",
]


def register_admin_routes(app: Flask, repository: PortalRepository) -> None:
    admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

    @admin_bp.before_request
    def load_admin_user() -> None:
        g.admin_user = None
        admin_user_id = session.get("admin_user_id")
        if not admin_user_id:
            return

        try:
            admin_user = repository.get_admin_user(int(admin_user_id))
        except Exception:
            admin_user = None

        if admin_user is None:
            clear_admin_session()
            return

        g.admin_user = admin_user

    @admin_bp.app_context_processor
    def inject_admin_context() -> dict[str, Any]:
        return {
            "admin_user": g.get("admin_user"),
            "admin_navigation": [
                {"label": "Dashboard", "endpoint": "admin.dashboard"},
                {"label": "Content", "endpoint": "admin.content_management"},
                {"label": "Incidents", "endpoint": "admin.incident_management"},
                {"label": "Licensing", "endpoint": "admin.licensing_management"},
                {"label": "Records", "endpoint": "admin.records_management"},
                {"label": "Research", "endpoint": "admin.research_management"},
                {"label": "Monitoring", "endpoint": "admin.monitoring"},
                {"label": "Activity", "endpoint": "admin.activity_log"},
            ],
        }

    def admin_login_required(view: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(view)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            if g.get("admin_user") is None:
                flash("Please sign in to access the administrator workspace.", "error")
                return redirect(url_for("admin.login", next=request.path))
            return view(*args, **kwargs)

        return wrapped

    def render_dashboard_page(db_error: str | None = None) -> str:
        try:
            context = repository.get_admin_dashboard_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_dashboard_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/dashboard.html",
            active_page="dashboard",
            db_error=current_db_error,
            **context,
        )

    def render_content_page(
        update_form_data: dict[str, str] | None = None,
        update_errors: list[str] | None = None,
        program_form_data: dict[str, str] | None = None,
        program_errors: list[str] | None = None,
        db_error: str | None = None,
    ) -> str:
        try:
            context = repository.get_admin_content_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_content_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/content.html",
            active_page="content",
            update_form_data=update_form_data or blank_update_form(),
            update_errors=update_errors or [],
            update_categories=UPDATE_CATEGORIES,
            program_form_data=program_form_data or blank_program_form(),
            program_errors=program_errors or [],
            program_statuses=PROGRAM_STATUSES,
            db_error=current_db_error,
            **context,
        )

    def render_incident_page(db_error: str | None = None) -> str:
        try:
            context = repository.get_admin_incident_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_incident_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/incidents.html",
            active_page="incidents",
            incident_statuses=INCIDENT_STATUSES,
            db_error=current_db_error,
            **context,
        )

    def render_licensing_page(
        service_form_data: dict[str, str] | None = None,
        service_errors: list[str] | None = None,
        db_error: str | None = None,
    ) -> str:
        try:
            context = repository.get_admin_licensing_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_licensing_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/licensing.html",
            active_page="licensing",
            application_statuses=APPLICATION_STATUSES,
            service_form_data=service_form_data or blank_license_service_form(),
            service_errors=service_errors or [],
            db_error=current_db_error,
            **context,
        )

    def render_records_page(db_error: str | None = None) -> str:
        try:
            context = repository.get_admin_records_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_records_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/records.html",
            active_page="records",
            db_error=current_db_error,
            **context,
        )

    def render_research_page(
        research_form_data: dict[str, str] | None = None,
        research_errors: list[str] | None = None,
        db_error: str | None = None,
    ) -> str:
        try:
            context = repository.get_admin_research_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_research_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/research.html",
            active_page="research",
            research_form_data=research_form_data or blank_research_form(),
            research_errors=research_errors or [],
            research_statuses=RESEARCH_STATUSES,
            db_error=current_db_error,
            **context,
        )

    def render_monitoring_page(db_error: str | None = None) -> str:
        try:
            context = repository.get_admin_monitoring_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_monitoring_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/monitoring.html",
            active_page="monitoring",
            public_routes=build_public_routes(),
            db_error=current_db_error,
            **context,
        )

    def render_activity_page(db_error: str | None = None) -> str:
        try:
            context = repository.get_admin_activity_context()
            current_db_error = db_error
        except Exception as exc:
            context = empty_admin_activity_context()
            current_db_error = db_error or admin_database_error_message(exc)

        return render_template(
            "admin/activity.html",
            active_page="activity",
            db_error=current_db_error,
            **context,
        )

    @admin_bp.route("/login", methods=["GET", "POST"])
    def login() -> str:
        if g.get("admin_user") is not None:
            return redirect(url_for("admin.dashboard"))

        form_data = {
            "identifier": normalize_inline_text(request.form.get("identifier", "")),
            "password": request.form.get("password", ""),
        }
        next_path = safe_next_path(request.values.get("next"))
        errors: list[str] = []

        if request.method == "POST":
            if not form_data["identifier"]:
                errors.append("Username or email is required.")
            if not form_data["password"]:
                errors.append("Password is required.")

            if not errors:
                try:
                    admin_user = repository.get_admin_user_by_login(form_data["identifier"])
                except Exception as exc:
                    return render_template(
                        "admin/login.html",
                        form_data=form_data,
                        errors=[],
                        next_path=next_path,
                        db_error=admin_database_error_message(exc),
                    )

                if admin_user is None or not check_password_hash(
                    admin_user["password_hash"], form_data["password"]
                ):
                    errors.append("Invalid sign-in details.")
                else:
                    try:
                        repository.record_admin_login(
                            admin_user["admin_user_id"], get_client_ip_address()
                        )
                    except Exception as exc:
                        return render_template(
                            "admin/login.html",
                            form_data=form_data,
                            errors=[],
                            next_path=next_path,
                            db_error=admin_database_error_message(exc),
                        )

                    session.clear()
                    session["admin_user_id"] = admin_user["admin_user_id"]
                    flash("Administrator session started.", "success")
                    return redirect(next_path or url_for("admin.dashboard"))

        return render_template(
            "admin/login.html",
            form_data=form_data,
            errors=errors,
            next_path=next_path,
            db_error=None,
        )

    @admin_bp.route("/logout", methods=["POST"])
    @admin_login_required
    def logout() -> Any:
        admin_user = g.admin_user
        try:
            repository.log_admin_activity(
                admin_user["admin_user_id"],
                "Authentication",
                "AdminUser",
                admin_user["admin_user_id"],
                "Administrator signed out.",
                get_client_ip_address(),
            )
        except Exception:
            pass

        clear_admin_session()
        flash("Administrator session ended.", "success")
        return redirect(url_for("admin.login"))

    @admin_bp.route("", strict_slashes=False)
    @admin_bp.route("/", strict_slashes=False)
    @admin_login_required
    def dashboard_root() -> Any:
        return redirect(url_for("admin.dashboard"))

    @admin_bp.route("/dashboard")
    @admin_login_required
    def dashboard() -> str:
        return render_dashboard_page()

    @admin_bp.route("/content")
    @admin_login_required
    def content_management() -> str:
        return render_content_page()

    @admin_bp.route("/content/updates/create", methods=["POST"])
    @admin_login_required
    def create_update() -> str:
        update_form_data = blank_update_form()
        update_form_data["county_id"] = normalize_inline_text(request.form.get("county_id", ""))
        update_form_data["title"] = normalize_inline_text(request.form.get("title", ""))
        update_form_data["summary"] = normalize_block_text(request.form.get("summary", ""))
        update_form_data["publish_date"] = normalize_inline_text(request.form.get("publish_date", ""))
        update_form_data["category"] = normalize_inline_text(request.form.get("category", ""))
        update_form_data["is_featured"] = "true" if request.form.get("is_featured") else ""

        errors = validate_update_form(update_form_data)
        if errors:
            return render_content_page(update_form_data=update_form_data, update_errors=errors)

        payload = {
            "county_id": parse_optional_int(update_form_data["county_id"]),
            "title": update_form_data["title"],
            "summary": update_form_data["summary"],
            "publish_date": update_form_data["publish_date"],
            "category": update_form_data["category"],
            "is_featured": update_form_data["is_featured"] == "true",
        }

        try:
            update_id = repository.create_public_update(payload)
            repository.log_admin_activity(
                g.admin_user["admin_user_id"],
                "Content management",
                "Update",
                update_id,
                f"Published update: {payload['title']}",
                get_client_ip_address(),
            )
            flash(f"Public notice #{update_id} created.", "success")
            return redirect(url_for("admin.content_management"))
        except Exception as exc:
            return render_content_page(
                update_form_data=update_form_data,
                update_errors=[],
                db_error=admin_database_error_message(exc),
            )

    @admin_bp.route("/content/programs/create", methods=["POST"])
    @admin_login_required
    def create_program() -> str:
        program_form_data = blank_program_form()
        program_form_data["county_id"] = normalize_inline_text(request.form.get("county_id", ""))
        program_form_data["title"] = normalize_inline_text(request.form.get("title", ""))
        program_form_data["status"] = normalize_inline_text(request.form.get("status", ""))
        program_form_data["budget_millions"] = normalize_inline_text(
            request.form.get("budget_millions", "")
        )
        program_form_data["beneficiaries"] = normalize_inline_text(
            request.form.get("beneficiaries", "")
        )
        program_form_data["summary"] = normalize_block_text(request.form.get("summary", ""))

        errors = validate_program_form(program_form_data)
        if errors:
            return render_content_page(program_form_data=program_form_data, program_errors=errors)

        payload = {
            "county_id": int(program_form_data["county_id"]),
            "title": program_form_data["title"],
            "status": program_form_data["status"],
            "budget_millions": float(program_form_data["budget_millions"]),
            "beneficiaries": int(program_form_data["beneficiaries"]),
            "summary": program_form_data["summary"],
        }

        try:
            program_id = repository.create_program(payload)
            repository.log_admin_activity(
                g.admin_user["admin_user_id"],
                "Content management",
                "Program",
                program_id,
                f"Created program: {payload['title']}",
                get_client_ip_address(),
            )
            flash(f"Program #{program_id} created.", "success")
            return redirect(url_for("admin.content_management"))
        except Exception as exc:
            return render_content_page(
                program_form_data=program_form_data,
                program_errors=[],
                db_error=admin_database_error_message(exc),
            )

    @admin_bp.route("/incidents")
    @admin_login_required
    def incident_management() -> str:
        return render_incident_page()

    @admin_bp.route("/incidents/<int:report_id>/update", methods=["POST"])
    @admin_login_required
    def update_incident(report_id: int) -> Any:
        status = normalize_inline_text(request.form.get("status", ""))
        review_notes = normalize_block_text(request.form.get("review_notes", ""))

        if status not in INCIDENT_STATUSES:
            flash("Choose a valid incident status.", "error")
            return redirect(url_for("admin.incident_management"))

        try:
            updated_id = repository.update_incident_management(
                report_id, status, review_notes or None
            )
            if updated_id is None:
                flash("Incident report was not found.", "error")
            else:
                repository.log_admin_activity(
                    g.admin_user["admin_user_id"],
                    "Incident management",
                    "IncidentReport",
                    updated_id,
                    f"Updated incident report #{updated_id} to {status}.",
                    get_client_ip_address(),
                )
                flash(f"Incident report #{updated_id} updated.", "success")
        except Exception as exc:
            flash(admin_database_error_message(exc), "error")

        return redirect(url_for("admin.incident_management"))

    @admin_bp.route("/licensing")
    @admin_login_required
    def licensing_management() -> str:
        return render_licensing_page()

    @admin_bp.route("/licensing/services/create", methods=["POST"])
    @admin_login_required
    def create_license_service() -> str:
        service_form_data = blank_license_service_form()
        for key in service_form_data:
            if key == "is_featured":
                service_form_data[key] = "true" if request.form.get(key) else ""
            else:
                normalizer = (
                    normalize_block_text
                    if key in {"summary", "requirements"}
                    else normalize_inline_text
                )
                service_form_data[key] = normalizer(request.form.get(key, ""))

        errors = validate_license_service_form(service_form_data)
        if errors:
            return render_licensing_page(
                service_form_data=service_form_data,
                service_errors=errors,
            )

        payload = {
            "county_id": parse_optional_int(service_form_data["county_id"]),
            "title": service_form_data["title"],
            "category": service_form_data["category"],
            "processing_window_days": int(service_form_data["processing_window_days"]),
            "fee_ksh": float(service_form_data["fee_ksh"]),
            "applies_to": service_form_data["applies_to"],
            "summary": service_form_data["summary"],
            "requirements": service_form_data["requirements"],
            "is_featured": service_form_data["is_featured"] == "true",
            "sort_order": int(service_form_data["sort_order"]),
        }

        try:
            service_id = repository.create_license_service(payload)
            repository.log_admin_activity(
                g.admin_user["admin_user_id"],
                "Licensing management",
                "LicensingService",
                service_id,
                f"Created licensing service: {payload['title']}",
                get_client_ip_address(),
            )
            flash(f"Licensing service #{service_id} created.", "success")
            return redirect(url_for("admin.licensing_management"))
        except Exception as exc:
            return render_licensing_page(
                service_form_data=service_form_data,
                service_errors=[],
                db_error=admin_database_error_message(exc),
            )

    @admin_bp.route("/licensing/applications/<int:application_id>/update", methods=["POST"])
    @admin_login_required
    def update_license_application(application_id: int) -> Any:
        status = normalize_inline_text(request.form.get("status", ""))
        review_notes = normalize_block_text(request.form.get("review_notes", ""))

        if status not in APPLICATION_STATUSES:
            flash("Choose a valid application status.", "error")
            return redirect(url_for("admin.licensing_management"))

        try:
            updated_id = repository.update_license_application_management(
                application_id, status, review_notes or None
            )
            if updated_id is None:
                flash("Licence application was not found.", "error")
            else:
                repository.log_admin_activity(
                    g.admin_user["admin_user_id"],
                    "Licensing management",
                    "LicenseApplication",
                    updated_id,
                    f"Updated licence application #{updated_id} to {status}.",
                    get_client_ip_address(),
                )
                flash(f"Licence application #{updated_id} updated.", "success")
        except Exception as exc:
            flash(admin_database_error_message(exc), "error")

        return redirect(url_for("admin.licensing_management"))

    @admin_bp.route("/records")
    @admin_login_required
    def records_management() -> str:
        return render_records_page()

    @admin_bp.route("/records/rebuild", methods=["POST"])
    @admin_login_required
    def rebuild_records() -> Any:
        try:
            summary = repository.rebuild_knowledge_index()
            repository.log_admin_activity(
                g.admin_user["admin_user_id"],
                "Records management",
                "KnowledgeIndex",
                None,
                "Rebuilt the records similarity index.",
                get_client_ip_address(),
            )
            flash(
                "Records index refreshed: "
                f"{summary['document_count']} documents and "
                f"{summary['index_row_count']} indexed values updated.",
                "success",
            )
        except Exception as exc:
            flash(admin_database_error_message(exc), "error")

        return redirect(url_for("admin.records_management"))

    @admin_bp.route("/research")
    @admin_login_required
    def research_management() -> str:
        return render_research_page()

    @admin_bp.route("/research/create", methods=["POST"])
    @admin_login_required
    def create_research() -> str:
        research_form_data = blank_research_form()
        for key in research_form_data:
            if key == "is_featured":
                research_form_data[key] = "true" if request.form.get(key) else ""
            else:
                normalizer = normalize_block_text if key == "summary" else normalize_inline_text
                research_form_data[key] = normalizer(request.form.get(key, ""))

        errors = validate_research_form(research_form_data)
        if errors:
            return render_research_page(
                research_form_data=research_form_data,
                research_errors=errors,
            )

        payload = {
            "county_id": parse_optional_int(research_form_data["county_id"]),
            "title": research_form_data["title"],
            "research_theme": research_form_data["research_theme"],
            "status": research_form_data["status"],
            "lead_office": research_form_data["lead_office"],
            "start_date": research_form_data["start_date"],
            "summary": research_form_data["summary"],
            "outputs": research_form_data["outputs"],
            "is_featured": research_form_data["is_featured"] == "true",
        }

        try:
            research_id = repository.create_research_activity(payload)
            repository.log_admin_activity(
                g.admin_user["admin_user_id"],
                "Research management",
                "ResearchActivity",
                research_id,
                f"Created research activity: {payload['title']}",
                get_client_ip_address(),
            )
            flash(f"Research activity #{research_id} created.", "success")
            return redirect(url_for("admin.research_management"))
        except Exception as exc:
            return render_research_page(
                research_form_data=research_form_data,
                research_errors=[],
                db_error=admin_database_error_message(exc),
            )

    @admin_bp.route("/research/<int:research_activity_id>/update", methods=["POST"])
    @admin_login_required
    def update_research(research_activity_id: int) -> Any:
        status = normalize_inline_text(request.form.get("status", ""))
        is_featured = request.form.get("is_featured") == "on"

        if status not in RESEARCH_STATUSES:
            flash("Choose a valid research status.", "error")
            return redirect(url_for("admin.research_management"))

        try:
            updated_id = repository.update_research_activity_management(
                research_activity_id, status, is_featured
            )
            if updated_id is None:
                flash("Research activity was not found.", "error")
            else:
                repository.log_admin_activity(
                    g.admin_user["admin_user_id"],
                    "Research management",
                    "ResearchActivity",
                    updated_id,
                    f"Updated research activity #{updated_id} to {status}.",
                    get_client_ip_address(),
                )
                flash(f"Research activity #{updated_id} updated.", "success")
        except Exception as exc:
            flash(admin_database_error_message(exc), "error")

        return redirect(url_for("admin.research_management"))

    @admin_bp.route("/monitoring")
    @admin_login_required
    def monitoring() -> str:
        return render_monitoring_page()

    @admin_bp.route("/activity")
    @admin_login_required
    def activity_log() -> str:
        return render_activity_page()

    def clear_admin_session() -> None:
        session.pop("admin_user_id", None)

    app.register_blueprint(admin_bp)


def blank_update_form() -> dict[str, str]:
    return {
        "county_id": "",
        "title": "",
        "summary": "",
        "publish_date": "",
        "category": "",
        "is_featured": "",
    }


def blank_program_form() -> dict[str, str]:
    return {
        "county_id": "",
        "title": "",
        "status": PROGRAM_STATUSES[0],
        "budget_millions": "",
        "beneficiaries": "",
        "summary": "",
    }


def blank_license_service_form() -> dict[str, str]:
    return {
        "county_id": "",
        "title": "",
        "category": "",
        "processing_window_days": "",
        "fee_ksh": "",
        "applies_to": "",
        "summary": "",
        "requirements": "",
        "sort_order": "",
        "is_featured": "",
    }


def blank_research_form() -> dict[str, str]:
    return {
        "county_id": "",
        "title": "",
        "research_theme": "",
        "status": RESEARCH_STATUSES[0],
        "lead_office": "",
        "start_date": "",
        "summary": "",
        "outputs": "",
        "is_featured": "",
    }


def validate_update_form(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if not form_data["title"]:
        errors.append("Notice title is required.")
    if len(form_data["summary"]) < 24:
        errors.append("Notice summary must be at least 24 characters long.")
    if not form_data["publish_date"]:
        errors.append("Publish date is required.")
    if not form_data["category"]:
        errors.append("Category is required.")
    return errors


def validate_program_form(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if not form_data["county_id"]:
        errors.append("County is required.")
    if not form_data["title"]:
        errors.append("Program title is required.")
    if form_data["status"] not in PROGRAM_STATUSES:
        errors.append("Choose a valid program status.")
    if not is_positive_number(form_data["budget_millions"]):
        errors.append("Budget must be a positive number.")
    if not is_positive_integer(form_data["beneficiaries"]):
        errors.append("Beneficiaries must be a positive whole number.")
    if len(form_data["summary"]) < 24:
        errors.append("Program summary must be at least 24 characters long.")
    return errors


def validate_license_service_form(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if not form_data["title"]:
        errors.append("Service title is required.")
    if not form_data["category"]:
        errors.append("Category is required.")
    if not is_positive_integer(form_data["processing_window_days"]):
        errors.append("Processing days must be a positive whole number.")
    if not is_non_negative_number(form_data["fee_ksh"]):
        errors.append("Fee must be zero or a positive number.")
    if not form_data["applies_to"]:
        errors.append("Applies to field is required.")
    if len(form_data["summary"]) < 24:
        errors.append("Service summary must be at least 24 characters long.")
    if len(form_data["requirements"]) < 24:
        errors.append("Requirements must be at least 24 characters long.")
    if not is_positive_integer(form_data["sort_order"]):
        errors.append("Sort order must be a positive whole number.")
    return errors


def validate_research_form(form_data: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if not form_data["title"]:
        errors.append("Research title is required.")
    if not form_data["research_theme"]:
        errors.append("Research theme is required.")
    if form_data["status"] not in RESEARCH_STATUSES:
        errors.append("Choose a valid research status.")
    if not form_data["lead_office"]:
        errors.append("Lead office is required.")
    if not form_data["start_date"]:
        errors.append("Start date is required.")
    if len(form_data["summary"]) < 24:
        errors.append("Research summary must be at least 24 characters long.")
    if len(form_data["outputs"]) < 12:
        errors.append("Expected outputs must be at least 12 characters long.")
    return errors


def empty_admin_dashboard_context() -> dict[str, Any]:
    return {
        "metrics": {
            "update_count": 0,
            "program_count": 0,
            "research_count": 0,
            "license_service_count": 0,
            "licensing_backlog_count": 0,
            "incident_backlog_count": 0,
            "knowledge_document_count": 0,
            "active_admin_count": 0,
            "activity_log_count": 0,
        },
        "recent_updates": [],
        "recent_incidents": [],
        "recent_applications": [],
        "recent_activity": [],
    }


def empty_admin_content_context() -> dict[str, Any]:
    return {
        "counties": [],
        "recent_updates": [],
        "recent_programs": [],
    }


def empty_admin_incident_context() -> dict[str, Any]:
    return {
        "status_summary": [],
        "incidents": [],
    }


def empty_admin_licensing_context() -> dict[str, Any]:
    return {
        "counties": [],
        "status_summary": [],
        "license_services": [],
        "applications": [],
    }


def empty_admin_records_context() -> dict[str, Any]:
    return {
        "summary": {
            "document_count": 0,
            "index_row_count": 0,
            "last_indexed_at": None,
            "dimension_count": 48,
        },
        "source_counts": [],
        "recent_documents": [],
    }


def empty_admin_research_context() -> dict[str, Any]:
    return {
        "counties": [],
        "status_summary": [],
        "research_activities": [],
    }


def empty_admin_monitoring_context() -> dict[str, Any]:
    return {
        "metrics": {
            "service_count": 0,
            "county_count": 0,
            "recent_notice_count": 0,
            "live_program_count": 0,
            "visible_research_count": 0,
            "featured_license_count": 0,
            "latest_notice_date": None,
            "latest_incident_date": None,
            "latest_application_date": None,
            "incident_backlog_count": 0,
            "licensing_backlog_count": 0,
        },
        "county_freshness": [],
        "latest_public_updates": [],
    }


def empty_admin_activity_context() -> dict[str, Any]:
    return {
        "admins": [],
        "activity_summary": [],
        "activity_log": [],
    }


def build_public_routes() -> list[dict[str, str]]:
    return [
        {"label": "Home page", "url": url_for("home")},
        {"label": "County directory", "url": url_for("counties")},
        {"label": "Licensing", "url": url_for("licensing")},
        {"label": "Research", "url": url_for("research")},
        {"label": "Records search", "url": url_for("knowledge_search")},
        {"label": "Incident desk", "url": url_for("incident_desk")},
        {"label": "Service guide", "url": url_for("database_guide")},
    ]


def safe_next_path(raw_path: str | None) -> str | None:
    if raw_path and raw_path.startswith("/admin"):
        return raw_path
    return None


def get_client_ip_address() -> str | None:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr


def normalize_inline_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_block_text(value: str) -> str:
    return " ".join(value.split())


def parse_optional_int(value: str) -> int | None:
    return int(value) if value else None


def is_positive_integer(value: str) -> bool:
    try:
        return int(value) > 0
    except ValueError:
        return False


def is_positive_number(value: str) -> bool:
    try:
        return float(value) > 0
    except ValueError:
        return False


def is_non_negative_number(value: str) -> bool:
    try:
        return float(value) >= 0
    except ValueError:
        return False


def admin_database_error_message(exc: Exception) -> str:
    return "Administrative data is temporarily unavailable. Please try again shortly."
