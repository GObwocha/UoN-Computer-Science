# Kenya Environment Portal

Python Flask school project inspired by public government websites and adapted for Kenya with all 47 counties plus a national disaster coordination location, licensing services, online licence applications, research activities and normalized vector search.

## Stack

- Python 3
- Flask
- SQL Server
- SSMS 22 for creating and checking the database
- `pyodbc` for SQL Server access from Flask

## Project layout

- `app.py`: Flask routes
- `repository.py`: SQL Server queries and inserts
- `templates/`: Jinja HTML templates
- `static/`: CSS and JavaScript
- `database/CreateKenyaEnvironmentPortal.sql`: database schema and seed data
- `.vscode/launch.json`: run/debug setup for VS Code

## Run in VS Code

1. Open this folder in VS Code.
2. This workspace already includes a local virtual environment in `.venv`.
3. If you want to rebuild it later, you can try:

```powershell
python -m venv .venv
```

4. Start the project with the prepared interpreter:

```powershell
.venv\Scripts\python.exe app.py
```

5. If you need to reinstall the dependencies into this same `.venv`, use:

```powershell
python -m pip install --target .venv\Lib\site-packages -r requirements.txt
```

6. Open `database/CreateKenyaEnvironmentPortal.sql` in SSMS 22 and run it.
7. If your SQL Server is not `localhost`, update the connection string in `config.py` or set `SQL_SERVER_CONNECTION`.
8. Common local SQL Server names to try are `localhost`, `.\SQLEXPRESS`, or `localhost\SQLEXPRESS`.
9. To debug from VS Code, open Run and Debug and choose `Python: Kenya Flask Portal` if you opened the project folder directly, or `Python: KenyaEnvironmentPortal` if you opened the parent `E` folder.

10. Open `http://127.0.0.1:5000`.

## New features

- `Licensing` page for permits, requirements, fees and processing windows
- `Licensing > Apply` form that inserts rows into `dbo.LicenseApplications`
- `Research` page for county-linked studies and monitoring activity
- `Knowledge Search` page that:
  - normalizes document text
  - generates embeddings in SQL Server
  - stores vectors in `dbo.KnowledgeDocuments` and `dbo.KnowledgeVectorIndex`
  - queries for similarity against indexed content

## Useful SSMS checks

```sql
SELECT COUNT(*) AS CountyCount FROM dbo.Counties;
SELECT COUNT(*) AS LicenseCount FROM dbo.LicensingServices;
SELECT COUNT(*) AS LicenseApplicationCount FROM dbo.LicenseApplications;
SELECT COUNT(*) AS ResearchCount FROM dbo.ResearchActivities;
SELECT COUNT(*) AS ResponseLocationCount FROM dbo.ResponseLocations;
SELECT TOP 10 * FROM dbo.Programs ORDER BY ProgramId DESC;
SELECT TOP 10 * FROM dbo.LicensingServices ORDER BY SortOrder, LicenseServiceId;
SELECT TOP 10 * FROM dbo.LicenseApplications ORDER BY SubmittedAt DESC;
SELECT TOP 10 * FROM dbo.ResearchActivities ORDER BY StartDate DESC;
SELECT COUNT(*) AS KnowledgeDocumentCount FROM dbo.KnowledgeDocuments;
SELECT COUNT(*) AS KnowledgeVectorRowCount FROM dbo.KnowledgeVectorIndex;
SELECT TOP 20 * FROM dbo.IncidentReports ORDER BY ReportedAt DESC;
```
