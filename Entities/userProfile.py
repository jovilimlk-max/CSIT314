
'''
What this code does?
- Initialise the User Profile database.
- Create new user profiles and check for duplicate names.
- Retrieve individual profiles and the complete profile listing.
- Support the User Profiles listing and frontend search functionality.
- Update existing user profile information.
- Suspend or reactivate user profiles.
- Prevent repeated suspension or reactivation.
- Count the total number of profiles for the dashboard.
- Combine create, update and status operations without duplicate SQL helper methods.
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

            # Exclude the selected profile when checking for duplicates
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

    # Create a new User Profile
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

        # Insert the new User Profile directly into the database
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # New profiles automatically receive active status
            cursor.execute("""
                INSERT INTO user_profiles
                (profile_name, description, status)
                VALUES (?, ?, 'active')
            """, (profile_name, description))

            connection.commit()

        # Handle duplicate names or other database constraints
        except sqlite3.IntegrityError:
            connection.rollback()

            return {
                "data": {
                    "success": False,
                    "message": "Unable to create profile. Please try again."
                },
                "status_code": 409
            }

        finally:
            connection.close()

        # Return the successful creation result
        return {
            "data": {
                "success": True,
                "message": "User profile created successfully."
            },
            "status_code": 201
        }

    # Retrieve all existing User Profiles
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

            return [
                dict(profile)
                for profile in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Handle the complete User Profiles listing process
    def view_all_profiles(self):

        # Retrieve all profiles from the database
        profiles = self.get_all_profiles()

        # Return the complete listing result
        return {
            "success": True,
            "profiles": profiles
        }, 200

    # Retrieve a specific User Profile using its ID
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

            return dict(profile) if profile else None

        finally:
            connection.close()

    # Handle the complete View User Profile process
    def view_profile(self, profile_id):

        # Retrieve the selected profile
        profile = self.get_profile_by_id(profile_id)

        # Return an error if the profile does not exist
        if profile is None:
            return {
                "success": False,
                "message": "User profile not found."
            }, 404

        # Return the selected profile information
        return {
            "success": True,
            "profile": profile
        }, 200

    # Update an existing User Profile
    def update_profile(self, profile_id, profile_details):

        # Retrieve validated information from the Controller
        profile_name = profile_details["profile_name"]
        description = profile_details["description"]

        # Check whether another profile uses the updated name
        if self.profile_name_exists(
            profile_name,
            exclude_id=profile_id
        ):
            return {
                "data": {
                    "success": False,
                    "message": "A profile with this name already exists."
                },
                "status_code": 409
            }

        # Update the User Profile directly in the database
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update only the profile details, not its status
            cursor.execute("""
                UPDATE user_profiles
                SET profile_name = ?,
                    description = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (profile_name, description, profile_id))

            # Handle a profile that could not be updated
            if cursor.rowcount == 0:
                connection.rollback()

                return {
                    "data": {
                        "success": False,
                        "message": "Unable to update profile. Please try again."
                    },
                    "status_code": 409
                }

            connection.commit()

        # Handle database constraint errors
        except sqlite3.IntegrityError:
            connection.rollback()

            return {
                "data": {
                    "success": False,
                    "message": "Unable to update profile. Please try again."
                },
                "status_code": 409
            }

        finally:
            connection.close()

        # Return the successful update result
        return {
            "data": {
                "success": True,
                "message": "User profile updated successfully."
            },
            "status_code": 200
        }

    # Suspend or reactivate a User Profile
    def change_profile_status(self, profile_id, action):

        # Retrieve the selected profile from the database
        profile = self.get_profile_by_id(profile_id)

        # Return an error if the profile cannot be found
        if profile is None:
            return {
                "data": {
                    "success": False,
                    "message": "User Profile not found."
                },
                "status_code": 404
            }

        current_status = profile["status"]

        # Determine the new status based on the requested action
        if action == "suspend":
            new_status = "suspended"
            success_message = "User Profile suspended successfully."

            # Prevent suspending an already suspended profile
            if current_status == "suspended":
                return {
                    "data": {
                        "success": False,
                        "message": "User Profile is already suspended."
                    },
                    "status_code": 409
                }

        elif action == "reactivate":
            new_status = "active"
            success_message = "User Profile reactivated successfully."

            # Prevent reactivating an already active profile
            if current_status == "active":
                return {
                    "data": {
                        "success": False,
                        "message": "User Profile is already active."
                    },
                    "status_code": 409
                }

        else:
            # Safeguard for an unrecognised action
            return {
                "data": {
                    "success": False,
                    "message": "Invalid profile status action."
                },
                "status_code": 400
            }

        # Update the profile status directly in the database
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update only when the new status differs
            cursor.execute("""
                UPDATE user_profiles
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND status != ?
            """, (new_status, profile_id, new_status))

            # Handle an unsuccessful status change
            if cursor.rowcount == 0:
                connection.rollback()

                return {
                    "data": {
                        "success": False,
                        "message": "Unable to update profile status. Please try again."
                    },
                    "status_code": 409
                }

            connection.commit()

        finally:
            connection.close()

        # Return the successful status change result
        return {
            "data": {
                "success": True,
                "message": success_message,
                "status": new_status
            },
            "status_code": 200
        }

    # Count all User Profiles for the User Admin Dashboard
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

    # Initialise the User Profile database
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
