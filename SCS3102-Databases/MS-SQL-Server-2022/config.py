import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "kenya-environment-portal-dev-key")
    SQL_SERVER_CONNECTION = os.getenv(
        "SQL_SERVER_CONNECTION",
        (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=localhost;"
            "Database=KenyaEnvironmentPortalDb;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
            "Encrypt=no;"
        ),
    )
