
'''
What this code does?
- Initialise the User Account database.
- Retrieve user accounts and account information.
- Authenticate users, including role and suspension checks.
- Check assigned User Profile status during login.
- Create new user accounts without an assigned User Profile.
- Update existing account details and optional profile assignments.
- Suspend or reactivate existing user accounts.
- Retrieve account counts and User Admin Dashboard statistics.
'''

import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash

from Entities.userProfile import UserProfile


class UserAccount:

    # Set the database file location
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

    # Handle the complete login authentication process
    def authenticate_login(self, login_details):

        # Retrieve the validated login details
        email = login_details["email"]
        password = login_details["password"]
        selected_role = login_details["role"]

        # Retrieve the registered account
        user = self.get_user_by_email(email)

        # Check whether the account exists and password matches
        if user is None or not self.verify_password(
            password,
            user["password_hash"]
        ):
            return {
                "data": {
                    "success": False,
                    "message": "Invalid email or password."
                },
                "status_code": 401
            }

        # Check whether the selected role matches the registered role
        if selected_role != user["role"]:
            return {
                "data": {
                    "success": False,
                    "message": "Invalid login credentials or user type."
                },
                "status_code": 401
            }

        # Check whether the individual account is active
        if user["status"] != "active":
            return {
                "data": {
                    "success": False,
                    "message": "Your account has been suspended. Please contact the administrator."
                },
                "status_code": 403
            }

        # Check the assigned User Profile, if one exists
        profile_id = user["profile_id"]

        if profile_id is not None:

            # Retrieve the assigned profile through the Entity layer
            user_profile = UserProfile()
            profile = user_profile.get_profile_by_id(profile_id)

            # Block login if the profile does not exist or is suspended
            if profile is None or profile["status"] != "active":
                return {
                    "data": {
                        "success": False,
                        "message": "Your assigned user profile is suspended or unavailable. Please contact the administrator."
                    },
                    "status_code": 403
                }

        # Return the authenticated user's information
        return {
            "data": {
                "success": True,
                "message": "Login successful.",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            },
            "status_code": 200
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

            return [
                dict(account)
                for account in cursor.fetchall()
            ]

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
        self,
        account_id,
        name,
        email,
        role,
        profile_id,
        password_hash=None
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
                """, (
                    name,
                    email,
                    role,
                    profile_id,
                    account_id
                ))

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
                    name,
                    email,
                    password_hash,
                    role,
                    profile_id,
                    account_id
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

    # Suspend or reactivate an existing user account
    def update_account_status(self, account_id, status):

        # Only allow the recognised account statuses
        if status not in {"active", "suspended"}:
            return False

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE user_accounts
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND status != ?
            """, (status, account_id, status))

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()
            return True

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

    # Count accounts with suspended status
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

    # Retrieve and prepare all User Admin Dashboard statistics
    def get_dashboard_statistics(self):

        # Retrieve User Account statistics
        total_accounts = self.get_total_accounts()
        suspended_accounts = self.get_suspended_accounts()

        # Retrieve User Profile statistics within the Entity layer
        user_profile = UserProfile()
        total_profiles = user_profile.get_total_profiles()

        # Return the complete result to the Controller
        return {
            "success": True,
            "statistics": {
                "total_accounts": total_accounts,
                "total_profiles": total_profiles,
                "suspended_accounts": suspended_accounts
            }
        }, 200

    # Initialise the User Account database
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
