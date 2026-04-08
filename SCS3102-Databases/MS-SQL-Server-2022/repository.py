from __future__ import annotations

from typing import Any

import pyodbc

VECTOR_DIMENSIONS = 48


class PortalRepository:
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def get_home_context(self) -> dict[str, Any]:
        metrics = self.fetch_one(
            """
            SELECT
                (SELECT COUNT(*) FROM dbo.Counties) AS county_count,
                (SELECT COUNT(*) FROM dbo.ResponseLocations) AS response_location_count,
                (SELECT COUNT(*) FROM dbo.LicensingServices) AS license_count,
                (SELECT COUNT(*) FROM dbo.ResearchActivities) AS research_activity_count,
                (SELECT COUNT(*) FROM dbo.LicenseApplications) AS license_application_count,
                (SELECT COUNT(*) FROM dbo.KnowledgeDocuments) AS knowledge_document_count,
                (SELECT COUNT(*) FROM dbo.KnowledgeVectorIndex) AS knowledge_index_row_count,
                (SELECT COUNT(*) FROM dbo.Programs) AS program_count,
                (SELECT COUNT(*) FROM dbo.IncidentReports) AS incident_count;
            """
        )

        return {
            "county_count": metrics["county_count"],
            "response_location_count": metrics["response_location_count"],
            "license_count": metrics["license_count"],
            "research_activity_count": metrics["research_activity_count"],
            "license_application_count": metrics["license_application_count"],
            "knowledge_document_count": metrics["knowledge_document_count"],
            "knowledge_index_row_count": metrics["knowledge_index_row_count"],
            "program_count": metrics["program_count"],
            "incident_count": metrics["incident_count"],
            "quick_services": self.fetch_all(
                """
                SELECT TOP 8
                    Title AS title,
                    Description AS description,
                    Controller AS controller,
                    Action AS action,
                    SearchTerm AS search_term
                FROM dbo.Services
                ORDER BY SortOrder;
                """
            ),
            "featured_updates": self.fetch_all(
                """
                SELECT TOP 3
                    u.UpdateId AS update_id,
                    u.Title AS title,
                    u.Summary AS summary,
                    u.PublishDate AS publish_date,
                    u.Category AS category,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.Updates u
                LEFT JOIN dbo.Counties c ON c.CountyId = u.CountyId
                WHERE u.IsFeatured = 1
                ORDER BY u.PublishDate DESC, u.UpdateId DESC;
                """
            ),
            "latest_updates": self.fetch_all(
                """
                SELECT TOP 6
                    u.UpdateId AS update_id,
                    u.Title AS title,
                    u.Summary AS summary,
                    u.PublishDate AS publish_date,
                    u.Category AS category,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.Updates u
                LEFT JOIN dbo.Counties c ON c.CountyId = u.CountyId
                ORDER BY u.PublishDate DESC, u.UpdateId DESC;
                """
            ),
            "featured_programs": self.fetch_all(
                """
                SELECT TOP 4
                    p.ProgramId AS program_id,
                    p.Title AS title,
                    p.Status AS status,
                    p.BudgetMillions AS budget_millions,
                    p.Beneficiaries AS beneficiaries,
                    p.Summary AS summary,
                    c.Name AS county_name
                FROM dbo.Programs p
                INNER JOIN dbo.Counties c ON c.CountyId = p.CountyId
                ORDER BY
                    CASE p.Status
                        WHEN N'Active' THEN 1
                        WHEN N'Planned' THEN 2
                        ELSE 3
                    END,
                    p.BudgetMillions DESC,
                    p.ProgramId;
                """
            ),
            "license_highlights": self.fetch_all(
                """
                SELECT TOP 4
                    ls.LicenseServiceId AS license_service_id,
                    ls.Title AS title,
                    ls.Category AS category,
                    ls.ProcessingWindowDays AS processing_window_days,
                    ls.FeeKsh AS fee_ksh,
                    ls.AppliesTo AS applies_to,
                    ls.Summary AS summary,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.LicensingServices ls
                LEFT JOIN dbo.Counties c ON c.CountyId = ls.CountyId
                WHERE ls.IsFeatured = 1
                ORDER BY ls.SortOrder, ls.LicenseServiceId;
                """
            ),
            "research_highlights": self.fetch_all(
                """
                SELECT TOP 4
                    ra.ResearchActivityId AS research_activity_id,
                    ra.Title AS title,
                    ra.ResearchTheme AS research_theme,
                    ra.Status AS status,
                    ra.LeadOffice AS lead_office,
                    ra.StartDate AS start_date,
                    ra.Summary AS summary,
                    ra.Outputs AS outputs,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.ResearchActivities ra
                LEFT JOIN dbo.Counties c ON c.CountyId = ra.CountyId
                WHERE ra.IsFeatured = 1
                ORDER BY ra.StartDate DESC, ra.ResearchActivityId DESC;
                """
            ),
            "recent_license_applications": self.fetch_all(
                """
                SELECT TOP 3
                    la.ApplicationId AS application_id,
                    la.ApplicantName AS applicant_name,
                    COALESCE(la.OrganizationName, N'Individual applicant') AS organization_name,
                    la.Status AS status,
                    la.SubmittedAt AS submitted_at,
                    ls.Title AS license_title,
                    COALESCE(c.Name, N'Unspecified county') AS county_name
                FROM dbo.LicenseApplications la
                INNER JOIN dbo.LicensingServices ls ON ls.LicenseServiceId = la.LicenseServiceId
                LEFT JOIN dbo.Counties c ON c.CountyId = la.ProjectCountyId
                ORDER BY la.SubmittedAt DESC, la.ApplicationId DESC;
                """
            ),
            "knowledge_index_summary": self.get_knowledge_index_summary(),
            "county_highlights": self.fetch_all(
                """
                SELECT TOP 8
                    c.CountyId AS county_id,
                    c.Name AS name,
                    c.Region AS region,
                    c.Headquarters AS headquarters,
                    c.EcosystemFocus AS ecosystem_focus,
                    c.RiskLevel AS risk_level,
                    c.Overview AS overview,
                    COUNT(p.ProgramId) AS program_count
                FROM dbo.Counties c
                LEFT JOIN dbo.Programs p ON p.CountyId = c.CountyId
                GROUP BY
                    c.CountyId,
                    c.Name,
                    c.Region,
                    c.Headquarters,
                    c.EcosystemFocus,
                    c.RiskLevel,
                    c.Overview
                ORDER BY
                    CASE c.RiskLevel
                        WHEN N'High' THEN 1
                        WHEN N'Medium' THEN 2
                        ELSE 3
                    END,
                    c.Name;
                """
            ),
        }

    def get_counties(self, search_term: str | None) -> list[dict[str, Any]]:
        normalized = search_term.strip() if search_term else None
        return self.fetch_all(
            """
            SELECT
                c.CountyId AS county_id,
                c.Name AS name,
                c.Region AS region,
                c.Headquarters AS headquarters,
                c.PopulationEstimate AS population_estimate,
                c.AreaSqKm AS area_sq_km,
                c.EcosystemFocus AS ecosystem_focus,
                c.RiskLevel AS risk_level,
                c.Overview AS overview,
                COUNT(p.ProgramId) AS program_count
            FROM dbo.Counties c
            LEFT JOIN dbo.Programs p ON p.CountyId = c.CountyId
            WHERE
                ? IS NULL
                OR c.Name LIKE N'%' + ? + N'%'
                OR c.Region LIKE N'%' + ? + N'%'
                OR c.EcosystemFocus LIKE N'%' + ? + N'%'
            GROUP BY
                c.CountyId,
                c.Name,
                c.Region,
                c.Headquarters,
                c.PopulationEstimate,
                c.AreaSqKm,
                c.EcosystemFocus,
                c.RiskLevel,
                c.Overview
            ORDER BY c.Name;
            """,
            [normalized, normalized, normalized, normalized],
        )

    def get_licensing_services(self, search_term: str | None) -> list[dict[str, Any]]:
        normalized = search_term.strip() if search_term else None
        return self.fetch_all(
            """
            SELECT
                ls.LicenseServiceId AS license_service_id,
                ls.Title AS title,
                ls.Category AS category,
                ls.ProcessingWindowDays AS processing_window_days,
                ls.FeeKsh AS fee_ksh,
                ls.AppliesTo AS applies_to,
                ls.Summary AS summary,
                ls.Requirements AS requirements,
                COALESCE(c.Name, N'National') AS county_name
            FROM dbo.LicensingServices ls
            LEFT JOIN dbo.Counties c ON c.CountyId = ls.CountyId
            WHERE
                ? IS NULL
                OR ls.Title LIKE N'%' + ? + N'%'
                OR ls.Category LIKE N'%' + ? + N'%'
                OR ls.AppliesTo LIKE N'%' + ? + N'%'
                OR COALESCE(c.Name, N'National') LIKE N'%' + ? + N'%'
            ORDER BY
                CASE WHEN ls.IsFeatured = 1 THEN 0 ELSE 1 END,
                ls.SortOrder,
                ls.Title;
            """,
            [normalized, normalized, normalized, normalized, normalized],
        )

    def get_research_activities(self, search_term: str | None) -> list[dict[str, Any]]:
        normalized = search_term.strip() if search_term else None
        return self.fetch_all(
            """
            SELECT
                ra.ResearchActivityId AS research_activity_id,
                ra.Title AS title,
                ra.ResearchTheme AS research_theme,
                ra.Status AS status,
                ra.LeadOffice AS lead_office,
                ra.StartDate AS start_date,
                ra.Summary AS summary,
                ra.Outputs AS outputs,
                COALESCE(c.Name, N'National') AS county_name
            FROM dbo.ResearchActivities ra
            LEFT JOIN dbo.Counties c ON c.CountyId = ra.CountyId
            WHERE
                ? IS NULL
                OR ra.Title LIKE N'%' + ? + N'%'
                OR ra.ResearchTheme LIKE N'%' + ? + N'%'
                OR ra.Status LIKE N'%' + ? + N'%'
                OR ra.LeadOffice LIKE N'%' + ? + N'%'
                OR COALESCE(c.Name, N'National') LIKE N'%' + ? + N'%'
            ORDER BY
                CASE WHEN ra.IsFeatured = 1 THEN 0 ELSE 1 END,
                ra.StartDate DESC,
                ra.ResearchActivityId DESC;
            """,
            [normalized, normalized, normalized, normalized, normalized, normalized],
        )

    def get_county_details(self, county_id: int) -> dict[str, Any] | None:
        county = self.fetch_one(
            """
            SELECT
                CountyId AS county_id,
                Name AS name,
                Region AS region,
                Headquarters AS headquarters,
                PopulationEstimate AS population_estimate,
                AreaSqKm AS area_sq_km,
                EcosystemFocus AS ecosystem_focus,
                RiskLevel AS risk_level,
                Overview AS overview,
                ContactPhone AS contact_phone,
                ContactEmail AS contact_email
            FROM dbo.Counties
            WHERE CountyId = ?;
            """,
            [county_id],
        )

        if county is None:
            return None

        county["programs"] = self.fetch_all(
            """
            SELECT TOP 8
                ProgramId AS program_id,
                Title AS title,
                Status AS status,
                BudgetMillions AS budget_millions,
                Beneficiaries AS beneficiaries,
                Summary AS summary
            FROM dbo.Programs
            WHERE CountyId = ?
            ORDER BY
                CASE Status
                    WHEN N'Active' THEN 1
                    WHEN N'Planned' THEN 2
                    ELSE 3
                END,
                BudgetMillions DESC,
                ProgramId;
            """,
            [county_id],
        )
        county["updates"] = self.fetch_all(
            """
            SELECT TOP 6
                u.UpdateId AS update_id,
                u.Title AS title,
                u.Summary AS summary,
                u.PublishDate AS publish_date,
                u.Category AS category,
                COALESCE(c.Name, N'National') AS county_name
            FROM dbo.Updates u
            LEFT JOIN dbo.Counties c ON c.CountyId = u.CountyId
            WHERE u.CountyId = ? OR u.CountyId IS NULL
            ORDER BY u.PublishDate DESC, u.UpdateId DESC;
            """,
            [county_id],
        )
        county["licenses"] = self.fetch_all(
            """
            SELECT TOP 6
                ls.LicenseServiceId AS license_service_id,
                ls.Title AS title,
                ls.Category AS category,
                ls.ProcessingWindowDays AS processing_window_days,
                ls.FeeKsh AS fee_ksh,
                ls.AppliesTo AS applies_to,
                ls.Summary AS summary,
                ls.Requirements AS requirements,
                COALESCE(c.Name, N'National') AS county_name
            FROM dbo.LicensingServices ls
            LEFT JOIN dbo.Counties c ON c.CountyId = ls.CountyId
            WHERE ls.CountyId = ? OR ls.CountyId IS NULL
            ORDER BY
                CASE WHEN ls.CountyId = ? THEN 0 ELSE 1 END,
                CASE WHEN ls.IsFeatured = 1 THEN 0 ELSE 1 END,
                ls.SortOrder,
                ls.Title;
            """,
            [county_id, county_id],
        )
        county["research_activities"] = self.fetch_all(
            """
            SELECT TOP 6
                ra.ResearchActivityId AS research_activity_id,
                ra.Title AS title,
                ra.ResearchTheme AS research_theme,
                ra.Status AS status,
                ra.LeadOffice AS lead_office,
                ra.StartDate AS start_date,
                ra.Summary AS summary,
                ra.Outputs AS outputs,
                COALESCE(c.Name, N'National') AS county_name
            FROM dbo.ResearchActivities ra
            LEFT JOIN dbo.Counties c ON c.CountyId = ra.CountyId
            WHERE ra.CountyId = ? OR ra.CountyId IS NULL
            ORDER BY
                CASE WHEN ra.CountyId = ? THEN 0 ELSE 1 END,
                CASE WHEN ra.IsFeatured = 1 THEN 0 ELSE 1 END,
                ra.StartDate DESC,
                ra.ResearchActivityId DESC;
            """,
            [county_id, county_id],
        )
        return county

    def get_license_application_context(self) -> dict[str, Any]:
        return {
            "license_services": self.fetch_all(
                """
                SELECT
                    LicenseServiceId AS license_service_id,
                    Title AS title,
                    Category AS category,
                    ProcessingWindowDays AS processing_window_days,
                    FeeKsh AS fee_ksh
                FROM dbo.LicensingServices
                ORDER BY
                    CASE WHEN IsFeatured = 1 THEN 0 ELSE 1 END,
                    SortOrder,
                    Title;
                """
            ),
            "counties": self.fetch_all(
                """
                SELECT
                    CountyId AS county_id,
                    Name AS name
                FROM dbo.Counties
                ORDER BY Name;
                """
            ),
            "recent_applications": self.fetch_all(
                """
                SELECT TOP 5
                    la.ApplicationId AS application_id,
                    la.ApplicantName AS applicant_name,
                    COALESCE(la.OrganizationName, N'Individual applicant') AS organization_name,
                    la.Status AS status,
                    la.SubmittedAt AS submitted_at,
                    ls.Title AS license_title,
                    COALESCE(c.Name, N'Unspecified county') AS county_name
                FROM dbo.LicenseApplications la
                INNER JOIN dbo.LicensingServices ls ON ls.LicenseServiceId = la.LicenseServiceId
                LEFT JOIN dbo.Counties c ON c.CountyId = la.ProjectCountyId
                ORDER BY la.SubmittedAt DESC, la.ApplicationId DESC;
                """
            ),
        }

    def create_license_application(self, form_data: dict[str, Any]) -> int:
        query = """
            INSERT INTO dbo.LicenseApplications
            (
                LicenseServiceId,
                ProjectCountyId,
                ApplicantName,
                ApplicantEmail,
                OrganizationName,
                ProjectLocation,
                ProjectSummary,
                SupportingDocuments,
                Status
            )
            OUTPUT INSERTED.ApplicationId
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                N'Submitted'
            );
        """

        return int(
            self.execute_scalar(
                query,
                [
                    form_data["license_service_id"],
                    form_data["project_county_id"],
                    form_data["applicant_name"],
                    form_data["applicant_email"],
                    form_data["organization_name"] or None,
                    form_data["project_location"],
                    form_data["project_summary"],
                    form_data["supporting_documents"],
                ],
            )
        )

    def get_knowledge_index_summary(self) -> dict[str, Any]:
        summary = self.fetch_one(
            """
            SELECT
                COUNT(*) AS document_count,
                MAX(IndexedAt) AS last_indexed_at
            FROM dbo.KnowledgeDocuments;
            """
        ) or {"document_count": 0, "last_indexed_at": None}

        index_row_count = self.fetch_one(
            "SELECT COUNT(*) AS index_row_count FROM dbo.KnowledgeVectorIndex;"
        ) or {"index_row_count": 0}

        return {
            "document_count": summary["document_count"],
            "index_row_count": index_row_count["index_row_count"],
            "last_indexed_at": summary["last_indexed_at"],
            "dimension_count": VECTOR_DIMENSIONS,
        }

    def rebuild_knowledge_index(self) -> dict[str, Any]:
        summary = self.fetch_one("EXEC dbo.RebuildKnowledgeIndex;")
        if summary is None:
            return self.get_knowledge_index_summary()
        summary["dimension_count"] = VECTOR_DIMENSIONS
        return summary

    def query_knowledge_similarity(
        self, query_text: str, limit: int = 8
    ) -> list[dict[str, Any]]:
        return self.fetch_all(
            f"""
            ;WITH QueryText AS
            (
                SELECT dbo.NormalizeKnowledgeText(?) AS NormalizedText
            ),
            QueryTokens AS
            (
                SELECT value AS token
                FROM QueryText
                CROSS APPLY STRING_SPLIT(NormalizedText, N' ')
                WHERE LEN(value) > 1
            ),
            QueryTokenCounts AS
            (
                SELECT token, COUNT(*) AS token_count
                FROM QueryTokens
                GROUP BY token
            ),
            QueryDimensionContributions AS
            (
                SELECT
                    (ABS(CONVERT(BIGINT, CHECKSUM(token, N'dim'))) % {VECTOR_DIMENSIONS}) + 1 AS dimension_number,
                    (CASE WHEN ABS(CONVERT(BIGINT, CHECKSUM(token, N'sign'))) % 2 = 0 THEN 1.0 ELSE -1.0 END) *
                    ((1.0 + LOG(CAST(token_count AS FLOAT))) *
                    (1.0 + CAST(CASE WHEN LEN(token) > 12 THEN 12 ELSE LEN(token) END AS FLOAT) / 12.0)) AS raw_value
                FROM QueryTokenCounts
            ),
            QueryDimensionSums AS
            (
                SELECT
                    dimension_number,
                    SUM(raw_value) AS raw_value
                FROM QueryDimensionContributions
                GROUP BY dimension_number
            ),
            QueryNorm AS
            (
                SELECT SQRT(SUM(raw_value * raw_value)) AS vector_norm
                FROM QueryDimensionSums
            ),
            QueryEmbedding AS
            (
                SELECT
                    qds.dimension_number,
                    qds.raw_value / qn.vector_norm AS query_value
                FROM QueryDimensionSums qds
                CROSS JOIN QueryNorm qn
                WHERE qn.vector_norm > 0
            ),
            SimilarityScores AS
            (
                SELECT
                    kvi.DocumentId,
                    SUM(kvi.DimensionValue * qe.query_value) AS similarity_score
                FROM dbo.KnowledgeVectorIndex kvi
                INNER JOIN QueryEmbedding qe ON qe.dimension_number = kvi.DimensionNumber
                GROUP BY kvi.DocumentId
            )
            SELECT TOP {int(limit)}
                kd.DocumentId AS document_id,
                kd.SourceType AS source_type,
                kd.Category AS category,
                kd.Title AS title,
                kd.Summary AS summary,
                kd.RouteEndpoint AS route_endpoint,
                kd.RouteRecordId AS route_record_id,
                COALESCE(c.Name, N'National') AS county_name,
                CAST(ROUND(ss.similarity_score, 4) AS DECIMAL(10, 4)) AS similarity_score
            FROM SimilarityScores ss
            INNER JOIN dbo.KnowledgeDocuments kd ON kd.DocumentId = ss.DocumentId
            LEFT JOIN dbo.Counties c ON c.CountyId = kd.CountyId
            WHERE ss.similarity_score > 0.05
            ORDER BY ss.similarity_score DESC, kd.Title;
            """,
            [query_text],
        )

    def get_response_locations(self) -> list[dict[str, Any]]:
        return self.fetch_all(
            """
            SELECT
                ResponseLocationId AS response_location_id,
                LocationName AS location_name,
                LocationType AS location_type,
                Headquarters AS headquarters
            FROM dbo.ResponseLocations
            ORDER BY
                CASE LocationType
                    WHEN N'National Coordination' THEN 0
                    ELSE 1
                END,
                LocationName;
            """
        )

    def create_incident_report(self, form_data: dict[str, Any]) -> int:
        query = """
            INSERT INTO dbo.IncidentReports
            (
                ReporterName,
                ReporterEmail,
                CountyId,
                ResponseLocationId,
                Category,
                Location,
                Description,
                Status
            )
            OUTPUT INSERTED.ReportId
            VALUES
            (
                ?,
                ?,
                (SELECT CountyId FROM dbo.ResponseLocations WHERE ResponseLocationId = ?),
                ?,
                ?,
                ?,
                ?,
                N'New'
            );
        """

        return int(
            self.execute_scalar(
                query,
                [
                    form_data["reporter_name"],
                    form_data["reporter_email"],
                    form_data["response_location_id"],
                    form_data["response_location_id"],
                    form_data["category"],
                    form_data["location"],
                    form_data["description"],
                ],
            )
        )

    def get_admin_user(self, admin_user_id: int) -> dict[str, Any] | None:
        return self.fetch_one(
            """
            SELECT
                AdminUserId AS admin_user_id,
                FullName AS full_name,
                Username AS username,
                Email AS email,
                RoleName AS role_name,
                IsActive AS is_active,
                LastLoginAt AS last_login_at,
                CreatedAt AS created_at
            FROM dbo.AdminUsers
            WHERE AdminUserId = ? AND IsActive = 1;
            """,
            [admin_user_id],
        )

    def get_admin_user_by_login(self, login_identifier: str) -> dict[str, Any] | None:
        normalized = login_identifier.strip()
        return self.fetch_one(
            """
            SELECT TOP 1
                AdminUserId AS admin_user_id,
                FullName AS full_name,
                Username AS username,
                Email AS email,
                PasswordHash AS password_hash,
                RoleName AS role_name,
                IsActive AS is_active,
                LastLoginAt AS last_login_at,
                CreatedAt AS created_at
            FROM dbo.AdminUsers
            WHERE
                IsActive = 1
                AND
                (
                    LOWER(Username) = LOWER(?)
                    OR LOWER(Email) = LOWER(?)
                );
            """,
            [normalized, normalized],
        )

    def record_admin_login(self, admin_user_id: int, ip_address: str | None) -> None:
        self.execute_non_query(
            """
            UPDATE dbo.AdminUsers
            SET LastLoginAt = SYSDATETIME()
            WHERE AdminUserId = ?;
            """,
            [admin_user_id],
        )
        self.log_admin_activity(
            admin_user_id,
            "Authentication",
            "AdminUser",
            admin_user_id,
            "Administrator signed in.",
            ip_address,
        )

    def log_admin_activity(
        self,
        admin_user_id: int,
        activity_type: str,
        entity_type: str,
        entity_id: int | None,
        description: str,
        ip_address: str | None = None,
    ) -> None:
        self.execute_non_query(
            """
            INSERT INTO dbo.AdminActivityLog
            (
                AdminUserId,
                ActivityType,
                EntityType,
                EntityId,
                Description,
                IpAddress
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            );
            """,
            [admin_user_id, activity_type, entity_type, entity_id, description, ip_address],
        )

    def get_admin_dashboard_context(self) -> dict[str, Any]:
        metrics = self.fetch_one(
            """
            SELECT
                (SELECT COUNT(*) FROM dbo.Updates) AS update_count,
                (SELECT COUNT(*) FROM dbo.Programs) AS program_count,
                (SELECT COUNT(*) FROM dbo.ResearchActivities) AS research_count,
                (SELECT COUNT(*) FROM dbo.LicensingServices) AS license_service_count,
                (SELECT COUNT(*) FROM dbo.LicenseApplications WHERE Status IN (N'Submitted', N'Under review')) AS licensing_backlog_count,
                (SELECT COUNT(*) FROM dbo.IncidentReports WHERE Status IN (N'New', N'Under review', N'Escalated')) AS incident_backlog_count,
                (SELECT COUNT(*) FROM dbo.KnowledgeDocuments) AS knowledge_document_count,
                (SELECT COUNT(*) FROM dbo.AdminUsers WHERE IsActive = 1) AS active_admin_count,
                (SELECT COUNT(*) FROM dbo.AdminActivityLog) AS activity_log_count;
            """
        ) or {}

        return {
            "metrics": metrics,
            "recent_updates": self.fetch_all(
                """
                SELECT TOP 6
                    u.UpdateId AS update_id,
                    u.Title AS title,
                    u.Category AS category,
                    u.PublishDate AS publish_date,
                    u.IsFeatured AS is_featured,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.Updates u
                LEFT JOIN dbo.Counties c ON c.CountyId = u.CountyId
                ORDER BY u.PublishDate DESC, u.UpdateId DESC;
                """
            ),
            "recent_incidents": self.fetch_all(
                """
                SELECT TOP 6
                    ir.ReportId AS report_id,
                    ir.Category AS category,
                    ir.Status AS status,
                    ir.Location AS location,
                    ir.ReportedAt AS reported_at,
                    COALESCE(c.Name, N'National') AS county_name,
                    rl.LocationName AS response_location_name
                FROM dbo.IncidentReports ir
                LEFT JOIN dbo.Counties c ON c.CountyId = ir.CountyId
                INNER JOIN dbo.ResponseLocations rl ON rl.ResponseLocationId = ir.ResponseLocationId
                ORDER BY ir.ReportedAt DESC, ir.ReportId DESC;
                """
            ),
            "recent_applications": self.fetch_all(
                """
                SELECT TOP 6
                    la.ApplicationId AS application_id,
                    la.ApplicantName AS applicant_name,
                    la.Status AS status,
                    la.SubmittedAt AS submitted_at,
                    ls.Title AS license_title,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.LicenseApplications la
                INNER JOIN dbo.LicensingServices ls ON ls.LicenseServiceId = la.LicenseServiceId
                LEFT JOIN dbo.Counties c ON c.CountyId = la.ProjectCountyId
                ORDER BY la.SubmittedAt DESC, la.ApplicationId DESC;
                """
            ),
            "recent_activity": self.fetch_all(
                """
                SELECT TOP 8
                    al.ActivityLogId AS activity_log_id,
                    al.ActivityType AS activity_type,
                    al.EntityType AS entity_type,
                    al.Description AS description,
                    al.OccurredAt AS occurred_at,
                    au.FullName AS admin_name
                FROM dbo.AdminActivityLog al
                INNER JOIN dbo.AdminUsers au ON au.AdminUserId = al.AdminUserId
                ORDER BY al.OccurredAt DESC, al.ActivityLogId DESC;
                """
            ),
        }

    def get_admin_content_context(self) -> dict[str, Any]:
        return {
            "counties": self.fetch_all(
                """
                SELECT
                    CountyId AS county_id,
                    Name AS name
                FROM dbo.Counties
                ORDER BY Name;
                """
            ),
            "recent_updates": self.fetch_all(
                """
                SELECT TOP 12
                    u.UpdateId AS update_id,
                    u.Title AS title,
                    u.Category AS category,
                    u.PublishDate AS publish_date,
                    u.IsFeatured AS is_featured,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.Updates u
                LEFT JOIN dbo.Counties c ON c.CountyId = u.CountyId
                ORDER BY u.PublishDate DESC, u.UpdateId DESC;
                """
            ),
            "recent_programs": self.fetch_all(
                """
                SELECT TOP 12
                    p.ProgramId AS program_id,
                    p.Title AS title,
                    p.Status AS status,
                    p.BudgetMillions AS budget_millions,
                    p.Beneficiaries AS beneficiaries,
                    c.Name AS county_name
                FROM dbo.Programs p
                INNER JOIN dbo.Counties c ON c.CountyId = p.CountyId
                ORDER BY p.ProgramId DESC;
                """
            ),
        }

    def create_public_update(self, form_data: dict[str, Any]) -> int:
        return int(
            self.execute_scalar(
                """
                INSERT INTO dbo.Updates
                (
                    CountyId,
                    Title,
                    Summary,
                    PublishDate,
                    Category,
                    IsFeatured
                )
                OUTPUT INSERTED.UpdateId
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                );
                """,
                [
                    form_data["county_id"],
                    form_data["title"],
                    form_data["summary"],
                    form_data["publish_date"],
                    form_data["category"],
                    form_data["is_featured"],
                ],
            )
        )

    def create_program(self, form_data: dict[str, Any]) -> int:
        return int(
            self.execute_scalar(
                """
                INSERT INTO dbo.Programs
                (
                    CountyId,
                    Title,
                    Status,
                    BudgetMillions,
                    Beneficiaries,
                    Summary
                )
                OUTPUT INSERTED.ProgramId
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                );
                """,
                [
                    form_data["county_id"],
                    form_data["title"],
                    form_data["status"],
                    form_data["budget_millions"],
                    form_data["beneficiaries"],
                    form_data["summary"],
                ],
            )
        )

    def get_admin_incident_context(self) -> dict[str, Any]:
        return {
            "status_summary": self.fetch_all(
                """
                SELECT
                    Status AS status,
                    COUNT(*) AS status_count
                FROM dbo.IncidentReports
                GROUP BY Status
                ORDER BY
                    CASE Status
                        WHEN N'New' THEN 0
                        WHEN N'Under review' THEN 1
                        WHEN N'Escalated' THEN 2
                        WHEN N'Closed' THEN 3
                        ELSE 4
                    END;
                """
            ),
            "incidents": self.fetch_all(
                """
                SELECT TOP 25
                    ir.ReportId AS report_id,
                    ir.ReporterName AS reporter_name,
                    ir.ReporterEmail AS reporter_email,
                    ir.Category AS category,
                    ir.Location AS location,
                    ir.Description AS description,
                    ir.Status AS status,
                    ir.ReviewNotes AS review_notes,
                    ir.ReportedAt AS reported_at,
                    ir.UpdatedAt AS updated_at,
                    COALESCE(c.Name, N'National') AS county_name,
                    rl.LocationName AS response_location_name
                FROM dbo.IncidentReports ir
                LEFT JOIN dbo.Counties c ON c.CountyId = ir.CountyId
                INNER JOIN dbo.ResponseLocations rl ON rl.ResponseLocationId = ir.ResponseLocationId
                ORDER BY ir.ReportedAt DESC, ir.ReportId DESC;
                """
            ),
        }

    def update_incident_management(
        self, report_id: int, status: str, review_notes: str | None
    ) -> int | None:
        updated_id = self.execute_scalar(
            """
            UPDATE dbo.IncidentReports
            SET
                Status = ?,
                ReviewNotes = ?,
                UpdatedAt = SYSDATETIME()
            OUTPUT INSERTED.ReportId
            WHERE ReportId = ?;
            """,
            [status, review_notes, report_id],
        )
        return int(updated_id) if updated_id is not None else None

    def get_admin_licensing_context(self) -> dict[str, Any]:
        return {
            "counties": self.fetch_all(
                """
                SELECT
                    CountyId AS county_id,
                    Name AS name
                FROM dbo.Counties
                ORDER BY Name;
                """
            ),
            "status_summary": self.fetch_all(
                """
                SELECT
                    Status AS status,
                    COUNT(*) AS status_count
                FROM dbo.LicenseApplications
                GROUP BY Status
                ORDER BY
                    CASE Status
                        WHEN N'Submitted' THEN 0
                        WHEN N'Under review' THEN 1
                        WHEN N'Approved' THEN 2
                        WHEN N'Rejected' THEN 3
                        ELSE 4
                    END;
                """
            ),
            "license_services": self.fetch_all(
                """
                SELECT TOP 15
                    ls.LicenseServiceId AS license_service_id,
                    ls.Title AS title,
                    ls.Category AS category,
                    ls.ProcessingWindowDays AS processing_window_days,
                    ls.FeeKsh AS fee_ksh,
                    ls.IsFeatured AS is_featured,
                    ls.SortOrder AS sort_order,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.LicensingServices ls
                LEFT JOIN dbo.Counties c ON c.CountyId = ls.CountyId
                ORDER BY
                    CASE WHEN ls.IsFeatured = 1 THEN 0 ELSE 1 END,
                    ls.SortOrder,
                    ls.Title;
                """
            ),
            "applications": self.fetch_all(
                """
                SELECT TOP 25
                    la.ApplicationId AS application_id,
                    la.ApplicantName AS applicant_name,
                    la.ApplicantEmail AS applicant_email,
                    COALESCE(la.OrganizationName, N'Individual applicant') AS organization_name,
                    la.ProjectLocation AS project_location,
                    la.ProjectSummary AS project_summary,
                    la.SupportingDocuments AS supporting_documents,
                    la.Status AS status,
                    la.ReviewNotes AS review_notes,
                    la.ReviewedAt AS reviewed_at,
                    la.SubmittedAt AS submitted_at,
                    ls.Title AS license_title,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.LicenseApplications la
                INNER JOIN dbo.LicensingServices ls ON ls.LicenseServiceId = la.LicenseServiceId
                LEFT JOIN dbo.Counties c ON c.CountyId = la.ProjectCountyId
                ORDER BY la.SubmittedAt DESC, la.ApplicationId DESC;
                """
            ),
        }

    def create_license_service(self, form_data: dict[str, Any]) -> int:
        return int(
            self.execute_scalar(
                """
                INSERT INTO dbo.LicensingServices
                (
                    CountyId,
                    Title,
                    Category,
                    ProcessingWindowDays,
                    FeeKsh,
                    AppliesTo,
                    Summary,
                    Requirements,
                    IsFeatured,
                    SortOrder
                )
                OUTPUT INSERTED.LicenseServiceId
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                );
                """,
                [
                    form_data["county_id"],
                    form_data["title"],
                    form_data["category"],
                    form_data["processing_window_days"],
                    form_data["fee_ksh"],
                    form_data["applies_to"],
                    form_data["summary"],
                    form_data["requirements"],
                    form_data["is_featured"],
                    form_data["sort_order"],
                ],
            )
        )

    def update_license_application_management(
        self, application_id: int, status: str, review_notes: str | None
    ) -> int | None:
        updated_id = self.execute_scalar(
            """
            UPDATE dbo.LicenseApplications
            SET
                Status = ?,
                ReviewNotes = ?,
                ReviewedAt = SYSDATETIME()
            OUTPUT INSERTED.ApplicationId
            WHERE ApplicationId = ?;
            """,
            [status, review_notes, application_id],
        )
        return int(updated_id) if updated_id is not None else None

    def get_admin_records_context(self) -> dict[str, Any]:
        return {
            "summary": self.get_knowledge_index_summary(),
            "source_counts": self.fetch_all(
                """
                SELECT
                    SourceType AS source_type,
                    COUNT(*) AS document_count,
                    MAX(IndexedAt) AS last_indexed_at
                FROM dbo.KnowledgeDocuments
                GROUP BY SourceType
                ORDER BY document_count DESC, source_type;
                """
            ),
            "recent_documents": self.fetch_all(
                """
                SELECT TOP 20
                    kd.DocumentId AS document_id,
                    kd.SourceType AS source_type,
                    kd.Category AS category,
                    kd.Title AS title,
                    kd.TokenCount AS token_count,
                    kd.IndexedAt AS indexed_at,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.KnowledgeDocuments kd
                LEFT JOIN dbo.Counties c ON c.CountyId = kd.CountyId
                ORDER BY kd.IndexedAt DESC, kd.DocumentId DESC;
                """
            ),
        }

    def get_admin_research_context(self) -> dict[str, Any]:
        return {
            "counties": self.fetch_all(
                """
                SELECT
                    CountyId AS county_id,
                    Name AS name
                FROM dbo.Counties
                ORDER BY Name;
                """
            ),
            "status_summary": self.fetch_all(
                """
                SELECT
                    Status AS status,
                    COUNT(*) AS status_count
                FROM dbo.ResearchActivities
                GROUP BY Status
                ORDER BY status_count DESC, status;
                """
            ),
            "research_activities": self.fetch_all(
                """
                SELECT TOP 20
                    ra.ResearchActivityId AS research_activity_id,
                    ra.Title AS title,
                    ra.ResearchTheme AS research_theme,
                    ra.Status AS status,
                    ra.LeadOffice AS lead_office,
                    ra.StartDate AS start_date,
                    ra.Outputs AS outputs,
                    ra.IsFeatured AS is_featured,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.ResearchActivities ra
                LEFT JOIN dbo.Counties c ON c.CountyId = ra.CountyId
                ORDER BY
                    CASE WHEN ra.IsFeatured = 1 THEN 0 ELSE 1 END,
                    ra.StartDate DESC,
                    ra.ResearchActivityId DESC;
                """
            ),
        }

    def create_research_activity(self, form_data: dict[str, Any]) -> int:
        return int(
            self.execute_scalar(
                """
                INSERT INTO dbo.ResearchActivities
                (
                    CountyId,
                    Title,
                    ResearchTheme,
                    Status,
                    LeadOffice,
                    StartDate,
                    Summary,
                    Outputs,
                    IsFeatured
                )
                OUTPUT INSERTED.ResearchActivityId
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                );
                """,
                [
                    form_data["county_id"],
                    form_data["title"],
                    form_data["research_theme"],
                    form_data["status"],
                    form_data["lead_office"],
                    form_data["start_date"],
                    form_data["summary"],
                    form_data["outputs"],
                    form_data["is_featured"],
                ],
            )
        )

    def update_research_activity_management(
        self, research_activity_id: int, status: str, is_featured: bool
    ) -> int | None:
        updated_id = self.execute_scalar(
            """
            UPDATE dbo.ResearchActivities
            SET
                Status = ?,
                IsFeatured = ?
            OUTPUT INSERTED.ResearchActivityId
            WHERE ResearchActivityId = ?;
            """,
            [status, is_featured, research_activity_id],
        )
        return int(updated_id) if updated_id is not None else None

    def get_admin_monitoring_context(self) -> dict[str, Any]:
        metrics = self.fetch_one(
            """
            SELECT
                (SELECT COUNT(*) FROM dbo.Services) AS service_count,
                (SELECT COUNT(*) FROM dbo.Counties) AS county_count,
                (SELECT COUNT(*) FROM dbo.Updates WHERE PublishDate >= DATEADD(DAY, -30, CAST(SYSDATETIME() AS DATE))) AS recent_notice_count,
                (SELECT COUNT(*) FROM dbo.Programs WHERE Status IN (N'Active', N'Monitoring')) AS live_program_count,
                (SELECT COUNT(*) FROM dbo.ResearchActivities WHERE Status IN (N'Active', N'Field analysis', N'Monitoring', N'Published')) AS visible_research_count,
                (SELECT COUNT(*) FROM dbo.LicensingServices WHERE IsFeatured = 1) AS featured_license_count,
                (SELECT MAX(PublishDate) FROM dbo.Updates) AS latest_notice_date,
                (SELECT MAX(ReportedAt) FROM dbo.IncidentReports) AS latest_incident_date,
                (SELECT MAX(SubmittedAt) FROM dbo.LicenseApplications) AS latest_application_date,
                (SELECT COUNT(*) FROM dbo.IncidentReports WHERE Status IN (N'New', N'Under review', N'Escalated')) AS incident_backlog_count,
                (SELECT COUNT(*) FROM dbo.LicenseApplications WHERE Status IN (N'Submitted', N'Under review')) AS licensing_backlog_count;
            """
        ) or {}

        return {
            "metrics": metrics,
            "county_freshness": self.fetch_all(
                """
                SELECT TOP 15
                    c.CountyId AS county_id,
                    c.Name AS county_name,
                    c.RiskLevel AS risk_level,
                    MAX(u.PublishDate) AS last_notice_date,
                    COUNT(DISTINCT u.UpdateId) AS notice_count,
                    COUNT(DISTINCT p.ProgramId) AS program_count,
                    COUNT(DISTINCT ra.ResearchActivityId) AS research_count
                FROM dbo.Counties c
                LEFT JOIN dbo.Updates u ON u.CountyId = c.CountyId
                LEFT JOIN dbo.Programs p ON p.CountyId = c.CountyId
                LEFT JOIN dbo.ResearchActivities ra ON ra.CountyId = c.CountyId
                GROUP BY c.CountyId, c.Name, c.RiskLevel
                ORDER BY
                    CASE WHEN MAX(u.PublishDate) IS NULL THEN 0 ELSE 1 END,
                    MAX(u.PublishDate),
                    CASE c.RiskLevel
                        WHEN N'High' THEN 0
                        WHEN N'Medium' THEN 1
                        ELSE 2
                    END,
                    c.Name;
                """
            ),
            "latest_public_updates": self.fetch_all(
                """
                SELECT TOP 6
                    u.UpdateId AS update_id,
                    u.Title AS title,
                    u.PublishDate AS publish_date,
                    u.Category AS category,
                    COALESCE(c.Name, N'National') AS county_name
                FROM dbo.Updates u
                LEFT JOIN dbo.Counties c ON c.CountyId = u.CountyId
                ORDER BY u.PublishDate DESC, u.UpdateId DESC;
                """
            ),
        }

    def get_admin_activity_context(self) -> dict[str, Any]:
        return {
            "admins": self.fetch_all(
                """
                SELECT
                    AdminUserId AS admin_user_id,
                    FullName AS full_name,
                    Username AS username,
                    Email AS email,
                    RoleName AS role_name,
                    IsActive AS is_active,
                    LastLoginAt AS last_login_at,
                    CreatedAt AS created_at
                FROM dbo.AdminUsers
                ORDER BY FullName;
                """
            ),
            "activity_summary": self.fetch_all(
                """
                SELECT TOP 8
                    ActivityType AS activity_type,
                    COUNT(*) AS activity_count
                FROM dbo.AdminActivityLog
                WHERE OccurredAt >= DATEADD(DAY, -30, SYSDATETIME())
                GROUP BY ActivityType
                ORDER BY activity_count DESC, activity_type;
                """
            ),
            "activity_log": self.fetch_all(
                """
                SELECT TOP 40
                    al.ActivityLogId AS activity_log_id,
                    al.ActivityType AS activity_type,
                    al.EntityType AS entity_type,
                    al.EntityId AS entity_id,
                    al.Description AS description,
                    al.IpAddress AS ip_address,
                    al.OccurredAt AS occurred_at,
                    au.FullName AS admin_name,
                    au.RoleName AS role_name
                FROM dbo.AdminActivityLog al
                INNER JOIN dbo.AdminUsers au ON au.AdminUserId = al.AdminUserId
                ORDER BY al.OccurredAt DESC, al.ActivityLogId DESC;
                """
            ),
        }

    def fetch_all(
        self, query: str, params: list[Any] | tuple[Any, ...] | None = None
    ) -> list[dict[str, Any]]:
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def fetch_one(
        self, query: str, params: list[Any] | tuple[Any, ...] | None = None
    ) -> dict[str, Any] | None:
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            row = cursor.fetchone()
            if row is None:
                return None
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))

    def execute_scalar(
        self, query: str, params: list[Any] | tuple[Any, ...] | None = None
    ) -> Any:
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            row = cursor.fetchone()
            connection.commit()
            return row[0] if row else None

    def execute_non_query(
        self, query: str, params: list[Any] | tuple[Any, ...] | None = None
    ) -> None:
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            connection.commit()

    def get_connection(self) -> pyodbc.Connection:
        return pyodbc.connect(self.connection_string)
