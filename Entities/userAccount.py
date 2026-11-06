
'''
What this code does?
- Initialise the User Account database.
- Authenticate users and check account and profile suspension.
- Create new user accounts with hashed passwords.
- Retrieve all accounts for listing, searching and filtering.
- Retrieve individual accounts with assigned User Profile details.
- Retrieve account information and available profiles for editing.
- Update account details, passwords and profile assignments.
- Suspend or reactivate accounts.
- Retrieve User Admin Dashboard statistics.
- Combine create, update and status operations without duplicate SQL helper methods.
'''

import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash

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

    # Handle the complete login authentication process
    def authenticate_login(self, login_details):

        email = login_details["email"]
        password = login_details["password"]
        selected_role = login_details["role"]

        # Retrieve the registered account
        user = self.get_user_by_email(email)

        # Check the email and password
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

        # Check the selected user role
        if selected_role != user["role"]:
            return {
                "data": {
                    "success": False,
                    "message": "Invalid login credentials or user type."
                },
                "status_code": 401
            }

        # Check the individual account status
        if user["status"] != "active":
            return {
                "data": {
                    "success": False,
                    "message": "Your account has been suspended. Please contact the administrator."
                },
                "status_code": 403
            }

        # Check the assigned profile, if any
        profile_id = user["profile_id"]

        if profile_id is not None:
            user_profile = UserProfile()
            profile = user_profile.get_profile_by_id(profile_id)

            if profile is None or profile["status"] != "active":
                return {
                    "data": {
                        "success": False,
                        "message": "Your assigned user profile is suspended or unavailable. Please contact the administrator."
                    },
                    "status_code": 403
                }

        # Return successful login details
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

    # Handle the complete Create User Account process
    def create_account(self, account_details):

        name = account_details["name"]
        email = account_details["email"]
        password = account_details["password"]
        role = account_details["role"]

        # Check whether the email is already registered
        if self.email_exists(email):
            return {
                "data": {
                    "success": False,
                    "message": "Email address is already registered."
                },
                "status_code": 409
            }

        # Hash the password without stripping it
        password_hash = generate_password_hash(password)

        # Insert the account directly with no assigned profile
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO user_accounts (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (name, email, password_hash, role))

            connection.commit()

        # Reject a duplicate email, including one inserted concurrently
        except sqlite3.IntegrityError:
            connection.rollback()
            return {
                "data": {
                    "success": False,
                    "message": "Email address is already registered."
                },
                "status_code": 409
            }

        finally:
            connection.close()

        return {
            "data": {
                "success": True,
                "message": "User account created successfully."
            },
            "status_code": 201
        }

    # Retrieve all accounts in ascending Account ID order
    def get_all_accounts(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id, name, email, role, status, profile_id
                FROM user_accounts
                ORDER BY id ASC
            """)

            return [
                dict(account)
                for account in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Handle the complete View All User Accounts process
    def view_all_accounts(self):

        # Retrieve all accounts from SQLite
        accounts = self.get_all_accounts()

        # Return account data to the Controller
        return {
            "success": True,
            "accounts": accounts
        }, 200

    # Retrieve a specific account using its ID
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

    # Handle the complete View User Account process
    def view_account(self, account_id):

        # Retrieve the selected account
        account = self.get_account_by_id(account_id)

        if account is None:
            return {
                "success": False,
                "message": "User account not found."
            }, 404

        # Retrieve the name of the assigned User Profile
        profile_id = account["profile_id"]

        if profile_id is not None:
            user_profile = UserProfile()
            profile = user_profile.get_profile_by_id(profile_id)

            account["profile_name"] = (
                profile["profile_name"]
                if profile else None
            )
        else:
            account["profile_name"] = None

        return {
            "success": True,
            "account": account
        }, 200

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

    # Retrieve existing account details and profiles for editing
    def get_account_update_details(self, account_id):

        # Retrieve the account with its assigned profile name
        account_result, status_code = self.view_account(account_id)

        if not account_result["success"]:
            return account_result, status_code

        # Retrieve available profiles from the User Profile Entity
        user_profile = UserProfile()
        profiles = user_profile.get_all_profiles()

        return {
            "success": True,
            "account": account_result["account"],
            "profiles": profiles
        }, 200

    # Handle the complete Update User Account process
    def update_account(self, account_id, account_details):

        name = account_details["name"]
        email = account_details["email"]
        password = account_details["password"]
        role = account_details["role"]
        profile_id = account_details["profile_id"]

        # Check for a duplicate email belonging to another account
        if self.email_exists(email, exclude_id=account_id):
            return {
                "data": {
                    "success": False,
                    "message": "Email address is already registered."
                },
                "status_code": 409
            }

        # Check the assigned profile if one was selected
        if profile_id is not None:
            user_profile = UserProfile()
            profile = user_profile.get_profile_by_id(profile_id)

            if profile is None:
                return {
                    "data": {
                        "success": False,
                        "message": "Selected user profile not found."
                    },
                    "status_code": 404
                }

        # Only hash the password when a new one is provided
        password_hash = None

        if password:
            password_hash = generate_password_hash(password)

        # Update the account directly in SQLite
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            if password_hash is None:

                # Preserve the existing password
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

                # Store the newly hashed password
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
                return {
                    "data": {
                        "success": False,
                        "message": "Unable to update account. Please try again."
                    },
                    "status_code": 409
                }

            connection.commit()

        except sqlite3.IntegrityError:
            connection.rollback()
            return {
                "data": {
                    "success": False,
                    "message": "Unable to update account. Please try again."
                },
                "status_code": 409
            }

        finally:
            connection.close()

        return {
            "data": {
                "success": True,
                "message": "User account updated successfully."
            },
            "status_code": 200
        }

    # Handle the complete Suspend / Reactivate process
    def change_account_status(self, account_id, action):

        # Retrieve the account and its current status
        account = self.get_account_by_id(account_id)

        if account is None:
            return {
                "data": {
                    "success": False,
                    "message": "User account not found."
                },
                "status_code": 404
            }

        current_status = account["status"]

        # Determine the new status and prevent repeated changes
        if action == "suspend":
            new_status = "suspended"
            success_message = "User account suspended successfully."

            if current_status == "suspended":
                return {
                    "data": {
                        "success": False,
                        "message": "User account is already suspended."
                    },
                    "status_code": 409
                }

        elif action == "reactivate":
            new_status = "active"
            success_message = "User account reactivated successfully."

            if current_status == "active":
                return {
                    "data": {
                        "success": False,
                        "message": "User account is already active."
                    },
                    "status_code": 409
                }

        else:
            return {
                "data": {
                    "success": False,
                    "message": "Invalid account status action."
                },
                "status_code": 400
            }

        # Update account status directly without changing profile status
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE user_accounts
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND status != ?
            """, (new_status, account_id, new_status))

            if cursor.rowcount == 0:
                connection.rollback()
                return {
                    "data": {
                        "success": False,
                        "message": "Unable to update account status. Please try again."
                    },
                    "status_code": 409
                }

            connection.commit()

        finally:
            connection.close()

        return {
            "data": {
                "success": True,
                "message": success_message,
                "status": new_status
            },
            "status_code": 200
        }

    # Count all User Accounts
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

    # Count suspended User Accounts
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

    # Retrieve Dashboard statistics
    def get_dashboard_statistics(self):

        total_accounts = self.get_total_accounts()
        suspended_accounts = self.get_suspended_accounts()

        # Retrieve the User Profile count from its Entity
        user_profile = UserProfile()
        total_profiles = user_profile.get_total_profiles()

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
