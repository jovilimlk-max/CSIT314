
'''
What this code does?
- Initialise the User Profile database.
- Create new user profiles and check for duplicate names.
- Retrieve all user profiles or a specific profile.
- Update existing user profile information.
- Suspend or reactivate existing user profiles.
- Count the total number of user profiles.
- Handle the complete Create User Profile database process.
'''

import sqlite3
from pathlib import Path


class UserProfile:

    # Set the database file location
    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "userProfile.db"
        )

    # Check whether a user profile name already exists
    def profile_name_exists(self, profile_name, exclude_id=None):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Exclude the current profile when checking for duplicates
            if exclude_id is not None:
                cursor.execute("""
                    SELECT id
                    FROM user_profiles
                    WHERE profile_name = ? COLLATE NOCASE
                    AND id != ?
                """, (profile_name, exclude_id))

            else:
                cursor.execute("""
                    SELECT id
                    FROM user_profiles
                    WHERE profile_name = ? COLLATE NOCASE
                """, (profile_name,))

            return cursor.fetchone() is not None

        finally:
            connection.close()

    # Handle the complete Create User Profile process
    def create_profile(self, profile_details):

        # Retrieve validated information from the Controller
        profile_name = profile_details["profile_name"]
        description = profile_details["description"]

        # Check whether the profile name already exists
        if self.profile_name_exists(profile_name):
            return {
                "data": {
                    "success": False,
                    "message": "A profile with this name already exists."
                },
                "status_code": 409
            }

        # Create the new profile in the database
        created = self.create_user_profile(
            profile_name,
            description
        )

        # Return an error if profile creation was unsuccessful
        if not created:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to create profile. Please try again."
                },
                "status_code": 409
            }

        # Return the successful creation result
        return {
            "data": {
                "success": True,
                "message": "User profile created successfully."
            },
            "status_code": 201
        }

    # Create a new user profile in the database
    def create_user_profile(self, profile_name, description):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # New profiles are automatically assigned active status
            cursor.execute("""
                INSERT INTO user_profiles
                (profile_name, description, status)
                VALUES (?, ?, 'active')
            """, (profile_name, description))

            connection.commit()
            return True

        except sqlite3.IntegrityError:
            connection.rollback()
            return False

        finally:
            connection.close()

    # Retrieve all existing user profiles
    def get_all_profiles(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id, profile_name, description, status
                FROM user_profiles
                ORDER BY profile_name ASC
            """)

            profiles = cursor.fetchall()

            # Convert database rows into dictionaries
            return [dict(profile) for profile in profiles]

        finally:
            connection.close()

    # Retrieve a specific user profile using its ID
    def get_profile_by_id(self, profile_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id, profile_name, description, status,
                       created_at, updated_at
                FROM user_profiles
                WHERE id = ?
            """, (profile_id,))

            profile = cursor.fetchone()

            if profile:
                return dict(profile)

            return None

        finally:
            connection.close()

    # Update an existing user profile in the database
    def update_user_profile(self, profile_id, profile_name, description):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update the profile information and timestamp
            cursor.execute("""
                UPDATE user_profiles
                SET profile_name = ?,
                    description = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (profile_name, description, profile_id))

            # Check whether an existing profile was updated
            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except sqlite3.IntegrityError:
            connection.rollback()
            return False

        finally:
            connection.close()

    # Suspend or reactivate an existing user profile
    def update_profile_status(self, profile_id, status):

        # Only allow recognised profile statuses
        if status not in {"active", "suspended"}:
            return False

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update only if the profile has a different status
            cursor.execute("""
                UPDATE user_profiles
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND status != ?
            """, (status, profile_id, status))

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()
            return True

        finally:
            connection.close()

    # Count all existing user profiles for the dashboard
    def get_total_profiles(self):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM user_profiles
            """)

            return cursor.fetchone()[0]

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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            connection.commit()

        finally:
            connection.close()
