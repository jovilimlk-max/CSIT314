'''
What this code does?
- Responsible for handling user account data and interacting with the database.
'''

import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash


class UserAccount:

    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "userAccount.db"
        )


    # Retrieve an account using the email
    def get_user_by_email(self, email):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Uses the SQL placeholder ? to pass the email safely rather than inserting it directly into the query
            cursor.execute(
                """
                SELECT id, email, password_hash, role, status
                FROM user_accounts
                WHERE email = ? COLLATE NOCASE
                """,
                (email,)
            )

            user = cursor.fetchone()

            if user:
                return dict(user)

            return None

        finally:
            connection.close()

    # Verify the password against its stored hash
    def verify_password(self, password, password_hash):
        return check_password_hash(password_hash, password)

    # Authenticate the user's credentials
    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)

        if user is None:
            return None

        if not self.verify_password(
            password, user["password_hash"]
        ):
            return None

        return {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "status": user["status"]
        }
    
    def initialise_database(self):
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                )
            """)

            connection.commit()

        finally:
            connection.close()

