
'''
What this code does?
- Initialise the IDP Category database table.
- Retrieve active categories available for IDP assignment.
- Retrieve an individual category using its Category ID.
- Check whether a category exists and is active.
- Support optional category assignment for Current and Past IDPs.
- Keep category database operations and domain checks in the Entity.
- Prepare the category structure for Platform Manager features in Sprint 5.
'''

import sqlite3
from pathlib import Path


class IDPCategory:

    # Use the existing Project database
    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "project.db"
        )

    # Initialise the IDP Category table
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
                    status TEXT NOT NULL DEFAULT 'active'
                )
            """)

            connection.commit()

        finally:
            connection.close()

    # Retrieve all active categories for IDP assignment
    def get_active_categories(self):

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Only active categories can be selected
            cursor.execute("""
                SELECT category_id, category_name
                FROM idp_categories
                WHERE status = 'active'
                ORDER BY category_name ASC
            """)

            # Return an empty list when no active categories exist
            return [
                dict(category)
                for category in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Retrieve an individual category
    def get_category_by_id(self, category_id):

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT category_id, category_name, status
                FROM idp_categories
                WHERE category_id = ?
            """, (category_id,))

            category = cursor.fetchone()

            return dict(category) if category else None

        finally:
            connection.close()

    # Check whether a category can be assigned to an IDP
    def is_active_category(self, category_id):

        # NULL is allowed because category assignment is optional
        if category_id is None:
            return True

        # Retrieve the selected category
        category = self.get_category_by_id(category_id)

        # Reject categories that do not exist
        if category is None:
            return False

        # Only active categories can be newly assigned
        return category["status"] == "active"
