
'''
What this code does?
- Handle user account data and interact with the database.
- Retrieve all user accounts or a specific account.
- Verify passwords and authenticate users.
- Create new user accounts without an assigned User Profile.
- Update existing user account details and optional profile assignment.
- Retrieve total and suspended user account counts.
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

    # Retrieve an account using its email
    def get_user_by_email(self, email):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, name, email, password_hash, role, status, profile_id
                FROM user_accounts
                WHERE email = ? COLLATE NOCASE
            """, (email,))

            user = cursor.fetchone()
            return dict(user) if user else None
        finally:
            connection.close()

    # Verify the entered password against the stored hash
    def verify_password(self, password, password_hash):
        return check_password_hash(password_hash, password)

    # Authenticate an account using its email and password
    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)

        if user is None:
            return None

        if not self.verify_password(password, user["password_hash"]):
            return None

        return {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "status": user["status"],
            "profile_id": user["profile_id"]
        }

    # Create an account without an assigned User Profile
    def create_user_account(self, name, email, password_hash, role):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO user_accounts (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (name, email, password_hash, role))

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
            cursor.execute("""
                SELECT id, name, email, role, status, profile_id
                FROM user_accounts
                ORDER BY id DESC
            """)

            return [dict(account) for account in cursor.fetchall()]
        finally:
            connection.close()

    # Retrieve a specific user account using its ID
    def get_account_by_id(self, account_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, name, email, role, status, profile_id, updated_at
                FROM user_accounts
                WHERE id = ?
            """, (account_id,))

            account = cursor.fetchone()
            return dict(account) if account else None
        finally:
            connection.close()

    # Check whether an email is used by another account
    def email_exists(self, email, exclude_id=None):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 1
                FROM user_accounts
                WHERE email = ? COLLATE NOCASE
                  AND (? IS NULL OR id != ?)
                LIMIT 1
            """, (email, exclude_id, exclude_id))

            return cursor.fetchone() is not None
        finally:
            connection.close()

    # Update an existing user account
    def update_user_account(
        self, account_id, name, email, role, profile_id, password_hash=None
    ):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            if password_hash is None:
                # Keep the existing password
                cursor.execute("""
                    UPDATE user_accounts
                    SET name = ?,
                        email = ?,
                        role = ?,
                        profile_id = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (name, email, role, profile_id, account_id))

            else:
                # Replace the password with its new hash
                cursor.execute("""
                    UPDATE user_accounts
                    SET name = ?,
                        email = ?,
                        password_hash = ?,
                        role = ?,
                        profile_id = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    name, email, password_hash,
                    role, profile_id, account_id
                ))

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()
            return True

        except sqlite3.IntegrityError:
            connection.rollback()
            return False

        finally:
            connection.close()

    # Count all user accounts
    def get_total_accounts(self):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM user_accounts
            """)

            return cursor.fetchone()[0]
        finally:
            connection.close()

    # Count user accounts with suspended status
    def get_suspended_accounts(self):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM user_accounts
                WHERE status = ?
            """, ("suspended",))

            return cursor.fetchone()[0]
        finally:
            connection.close()

    # Initialise the user account database
    def initialise_database(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
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
            """)

            connection.commit()
        finally:
            connection.close()
