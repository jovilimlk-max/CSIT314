
'''
What this code does?
- Initialise the separate IDP Category database.
- Store categories in Database/idpCategory.db.
- Create IDP categories with a name and description.
- Retrieve all categories for Platform Manager.
- Retrieve an individual category by Category ID.
- Update an existing category.
- Suspend or reactivate an IDP category.
- Prevent duplicate category names.
- Retrieve active categories for Interior Designer IDP assignment.
- Check whether a category is active.
- Keep database operations and domain checks in the Entity.
'''

import sqlite3
from pathlib import Path


class IDPCategory:

    # Use the separate IDP Category database
    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "idpCategory.db"
        )

    # Initialise the IDP Category database
    def initialise_database(self):

        # Create the Database folder if it does not exist
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Create the category table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS idp_categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    category_description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active', 'suspended'))
                )
            """)

            connection.commit()

        finally:
            connection.close()

    # Retrieve all IDP categories for Platform Manager
    def get_all_categories(self):

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    category_id,
                    category_name,
                    category_description,
                    status
                FROM idp_categories
                ORDER BY category_id ASC
            """)

            return [
                dict(category)
                for category in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Retrieve an individual IDP category
    def get_category_by_id(self, category_id):

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    category_id,
                    category_name,
                    category_description,
                    status
                FROM idp_categories
                WHERE category_id = ?
            """, (category_id,))

            category = cursor.fetchone()

            return dict(category) if category else None

        finally:
            connection.close()

    # Check whether a category name already exists
    def category_name_exists(
        self,
        category_name,
        exclude_category_id=None
    ):

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            if exclude_category_id is None:
                cursor.execute("""
                    SELECT 1
                    FROM idp_categories
                    WHERE category_name = ? COLLATE NOCASE
                    LIMIT 1
                """, (category_name,))

            else:
                cursor.execute("""
                    SELECT 1
                    FROM idp_categories
                    WHERE category_name = ? COLLATE NOCASE
                      AND category_id != ?
                    LIMIT 1
                """, (
                    category_name,
                    exclude_category_id
                ))

            return cursor.fetchone() is not None

        finally:
            connection.close()

    # Create a new IDP category
    def create_category(self, category_details):

        category_name = category_details["category_name"]
        category_description = category_details["category_description"]

        # Prevent duplicate category names
        if self.category_name_exists(category_name):
            return {
                "success": False,
                "message": "An IDP category with this name already exists."
            }, 409

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO idp_categories (
                    category_name,
                    category_description,
                    status
                )
                VALUES (?, ?, 'active')
            """, (
                category_name,
                category_description
            ))

            category_id = cursor.lastrowid

            connection.commit()

            return {
                "success": True,
                "message": "IDP category created successfully.",
                "category_id": category_id
            }, 201

        # Handle duplicate names at database level
        except sqlite3.IntegrityError:
            connection.rollback()

            return {
                "success": False,
                "message": "An IDP category with this name already exists."
            }, 409

        finally:
            connection.close()

    # Update an existing IDP category
    def update_category(self, category_details):

        category_id = category_details["category_id"]
        category_name = category_details["category_name"]
        category_description = category_details["category_description"]

        # Check whether the category exists
        category = self.get_category_by_id(category_id)

        if category is None:
            return {
                "success": False,
                "message": "IDP category not found."
            }, 404

        # Prevent duplicate category names
        if self.category_name_exists(
            category_name,
            category_id
        ):
            return {
                "success": False,
                "message": "An IDP category with this name already exists."
            }, 409

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update information without changing the category status
            cursor.execute("""
                UPDATE idp_categories
                SET
                    category_name = ?,
                    category_description = ?
                WHERE category_id = ?
            """, (
                category_name,
                category_description,
                category_id
            ))

            connection.commit()

            return {
                "success": True,
                "message": "IDP category updated successfully."
            }, 200

        except sqlite3.IntegrityError:
            connection.rollback()

            return {
                "success": False,
                "message": "An IDP category with this name already exists."
            }, 409

        finally:
            connection.close()

    # Suspend or reactivate an IDP category
    def change_category_status(self, category_id, new_status):

        # Check supported status values
        if new_status not in ("active", "suspended"):
            return {
                "success": False,
                "message": "Invalid category status."
            }, 400

        # Retrieve the existing category
        category = self.get_category_by_id(category_id)

        if category is None:
            return {
                "success": False,
                "message": "IDP category not found."
            }, 404

        # Prevent unnecessary status changes
        if category["status"] == new_status:
            return {
                "success": False,
                "message": f"IDP category is already {new_status}."
            }, 409

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update category status only
            cursor.execute("""
                UPDATE idp_categories
                SET status = ?
                WHERE category_id = ?
            """, (
                new_status,
                category_id
            ))

            connection.commit()

            if new_status == "suspended":
                message = "IDP category suspended successfully."
            else:
                message = "IDP category reactivated successfully."

            return {
                "success": True,
                "message": message
            }, 200

        finally:
            connection.close()

    # Retrieve active categories for Interior Designer assignment
    def get_active_categories(self):

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Suspended categories cannot be newly assigned
            cursor.execute("""
                SELECT category_id, category_name
                FROM idp_categories
                WHERE status = 'active'
                ORDER BY category_name COLLATE NOCASE ASC
            """)

            return [
                dict(category)
                for category in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Check whether a category can be assigned to an IDP
    def is_active_category(self, category_id):

        # Category assignment is optional
        if category_id is None:
            return True

        # Retrieve the selected category
        category = self.get_category_by_id(category_id)

        if category is None:
            return False

        return category["status"] == "active"
