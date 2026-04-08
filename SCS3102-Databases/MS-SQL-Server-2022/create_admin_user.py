from __future__ import annotations

from getpass import getpass

from werkzeug.security import generate_password_hash

from config import Config
from repository import PortalRepository


def prompt_value(label: str, default: str = "") -> str:
    prompt = f"{label}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    value = input(prompt).strip()
    return value or default


def main() -> None:
    repository = PortalRepository(Config.SQL_SERVER_CONNECTION)

    print("Create or update an administrator account")
    print("Leave a field blank to keep the suggested default where provided.")

    full_name = prompt_value("Full name")
    username = prompt_value("Username")
    email = prompt_value("Email address")
    role_name = prompt_value("Role name", "Super Administrator")

    while True:
        password = getpass("Password: ").strip()
        confirm_password = getpass("Confirm password: ").strip()

        if not full_name or not username or not email:
            raise ValueError("Full name, username and email are required.")

        if "@" not in email:
            raise ValueError("Enter a valid email address.")

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            continue

        if password != confirm_password:
            print("Passwords do not match. Try again.")
            continue

        break

    password_hash = generate_password_hash(password)

    existing_admin = repository.fetch_one(
        """
        SELECT TOP 1
            AdminUserId AS admin_user_id
        FROM dbo.AdminUsers
        WHERE
            LOWER(Username) = LOWER(?)
            OR LOWER(Email) = LOWER(?);
        """,
        [username, email],
    )

    if existing_admin:
        repository.execute_non_query(
            """
            UPDATE dbo.AdminUsers
            SET
                FullName = ?,
                Username = ?,
                Email = ?,
                PasswordHash = ?,
                RoleName = ?,
                IsActive = 1
            WHERE AdminUserId = ?;
            """,
            [
                full_name,
                username,
                email,
                password_hash,
                role_name,
                existing_admin["admin_user_id"],
            ],
        )
        print(f"Updated administrator account #{existing_admin['admin_user_id']}.")
        return

    admin_user_id = repository.execute_scalar(
        """
        INSERT INTO dbo.AdminUsers
        (
            FullName,
            Username,
            Email,
            PasswordHash,
            RoleName,
            IsActive
        )
        OUTPUT INSERTED.AdminUserId
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            1
        );
        """,
        [full_name, username, email, password_hash, role_name],
    )
    print(f"Created administrator account #{admin_user_id}.")


if __name__ == "__main__":
    main()
