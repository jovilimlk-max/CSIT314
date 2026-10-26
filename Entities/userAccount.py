
'''
What this code does?
- Handle user account data and interact with the database.
- Retrieve all user accounts or a specific account.
- Verify passwords and authenticate users.
- Create new user accounts without an assigned User Profile.
- Store account status, optional profile assignment and last updated date.
- Initialise the database.
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

            cursor.execute(
                """
                SELECT id, name, email, password_hash,
                       role, status, profile_id
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
            "status": user["status"],
            "profile_id": user["profile_id"]
        }

    # Create a new user account in the database
    def create_user_account(self, name, email, password_hash, role):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO user_accounts
                (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, password_hash, role)
            )

            connection.commit()
            return True

        except sqlite3.IntegrityError:
            connection.rollback()
            return False

        finally:
            connection.close()

    # Retrieve all existing user accounts
    def get_all_accounts(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id, name, email, role, status, profile_id
                FROM user_accounts
                ORDER BY id DESC
                """
            )

            accounts = cursor.fetchall()

            return [dict(account) for account in accounts]

        finally:
            connection.close()

    # Retrieve a specific user account using its ID
    def get_account_by_id(self, account_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id, name, email, role, status,
                       profile_id, updated_at
                FROM user_accounts
                WHERE id = ?
                """,
                (account_id,)
            )

            account = cursor.fetchone()

            if account:
                return dict(account)

            return None

        finally:
            connection.close()

    # Initialise the database
    def initialise_database(self):
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    profile_id INTEGER DEFAULT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

        finally:
            connection.close()
