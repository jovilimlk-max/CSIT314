
'''
What this code does?
- Responsible for handling user profile data and interacting with the database.
- Create new user profiles.
- Check whether a user profile name already exists.
- Retrieve all user profiles.
- Retrieve a specific user profile using its ID.
- Set newly created profiles to Active by default.
- Initialise the database.
'''

import sqlite3
from pathlib import Path


class UserProfile:

    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "userProfile.db"
        )

    # Check whether a user profile name already exists
    def profile_name_exists(self, profile_name):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # COLLATE NOCASE allows case-insensitive comparison
            cursor.execute(
                """
                SELECT id
                FROM user_profiles
                WHERE profile_name = ? COLLATE NOCASE
                """,
                (profile_name,)
            )

            return cursor.fetchone() is not None

        finally:
            connection.close()

    # Create a new user profile in the database
    def create_user_profile(self, profile_name, description):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # New profiles are automatically assigned Active status
            cursor.execute(
                """
                INSERT INTO user_profiles
                (profile_name, description, status)
                VALUES (?, ?, 'Active')
                """,
                (profile_name, description)
            )

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

        # Allow database rows to be accessed using column names
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id, profile_name, description, status
                FROM user_profiles
                ORDER BY profile_name ASC
                """
            )

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

            # Use a placeholder to safely retrieve the selected profile
            cursor.execute(
                """
                SELECT id, profile_name, description, status,
                       created_at, updated_at
                FROM user_profiles
                WHERE id = ?
                """,
                (profile_id,)
            )

            profile = cursor.fetchone()

            if profile:
                return dict(profile)

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
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

        finally:
            connection.close()
