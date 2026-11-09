
'''
What this code does?
- Initialise the database table for Customer saved IDPs.
- Allow Customers to save and unsave active projects.
- Prevent duplicate saves by the same Customer.
- Check whether a Customer has saved an IDP.
- Retrieve active IDPs saved by a Customer.
- Search, filter and sort the Customer's Saved List.
- Retrieve category and PIC information for saved projects.
- Preserve saved records when projects are suspended.
- Count how many Customers currently have an IDP saved.
'''

import os
import sqlite3


class SavedProject:

    def __init__(self):

        base_dir = os.path.dirname(os.path.dirname(__file__))

        self.database_path = os.path.join(
            base_dir,
            "Database",
            "project.db"
        )

        self.company_database_path = os.path.join(
            base_dir,
            "Database",
            "companyInformation.db"
        )

        self.account_database_path = os.path.join(
            base_dir,
            "Database",
            "userAccount.db"
        )

    # Initialise the saved projects table
    def initialise_database(self):

        os.makedirs(
            os.path.dirname(self.database_path),
            exist_ok=True
        )

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_projects (
                    saved_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    project_id INTEGER NOT NULL,
                    UNIQUE (account_id, project_id),
                    FOREIGN KEY (project_id)
                        REFERENCES projects(project_id)
                )
            ''')

            connection.commit()

        finally:
            connection.close()

    # Save an active IDP for a Customer
    def save_project(self, save_details):

        account_id = save_details["account_id"]
        project_id = save_details["project_id"]

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Only active IDPs can be saved
            cursor.execute('''
                SELECT project_id
                FROM projects
                WHERE project_id = ?
                  AND status = 'active'
            ''', (project_id,))

            project = cursor.fetchone()

            if project is None:
                return {
                    "success": False,
                    "message": "Project not found or unavailable."
                }, 404

            # Each Customer can save an IDP only once at a time
            cursor.execute('''
                SELECT saved_id
                FROM saved_projects
                WHERE account_id = ?
                  AND project_id = ?
            ''', (
                account_id,
                project_id
            ))

            if cursor.fetchone() is not None:
                return {
                    "success": False,
                    "message": "You have already saved this project."
                }, 400

            cursor.execute('''
                INSERT INTO saved_projects (
                    account_id,
                    project_id
                )
                VALUES (?, ?)
            ''', (
                account_id,
                project_id
            ))

            connection.commit()

            return {
                "success": True,
                "message": "Project saved successfully.",
                "project_id": project_id,
                "saved": True
            }, 201

        except sqlite3.IntegrityError:

            return {
                "success": False,
                "message": "You have already saved this project."
            }, 400

        finally:
            connection.close()

    # Remove an IDP from the Customer's saved list
    def unsave_project(self, save_details):

        account_id = save_details["account_id"]
        project_id = save_details["project_id"]

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute('''
                DELETE FROM saved_projects
                WHERE account_id = ?
                  AND project_id = ?
            ''', (
                account_id,
                project_id
            ))

            removed = cursor.rowcount > 0

            if not removed:
                return {
                    "success": False,
                    "message": "This project is not in your saved list."
                }, 404

            connection.commit()

            return {
                "success": True,
                "message": "Project removed from saved list.",
                "project_id": project_id,
                "saved": False
            }, 200

        finally:
            connection.close()

    # Check whether a Customer has saved an IDP
    def is_project_saved(self, account_id, project_id):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT saved_id
                FROM saved_projects
                WHERE account_id = ?
                  AND project_id = ?
            ''', (
                account_id,
                project_id
            ))

            return cursor.fetchone() is not None

        finally:
            connection.close()

    # Retrieve PIC names for the Customer's Saved List
    def get_saved_project_pics(self, projects):

        if not projects:
            return projects

        company_ids = {
            project["company_id"]
            for project in projects
        }

        company_connection = sqlite3.connect(
            self.company_database_path
        )

        company_connection.row_factory = sqlite3.Row

        try:
            cursor = company_connection.cursor()

            placeholders = ",".join(
                "?" for _ in company_ids
            )

            # Retrieve the Interior Designer account for each company
            cursor.execute(f'''
                SELECT
                    company_id,
                    account_id,
                    status AS company_status
                FROM company_information
                WHERE company_id IN ({placeholders})
            ''', tuple(company_ids))

            companies = {
                company["company_id"]: dict(company)
                for company in cursor.fetchall()
            }

        finally:
            company_connection.close()

        account_ids = {
            company["account_id"]
            for company in companies.values()
        }

        account_names = {}

        if account_ids:

            account_connection = sqlite3.connect(
                self.account_database_path
            )

            account_connection.row_factory = sqlite3.Row

            try:
                cursor = account_connection.cursor()

                placeholders = ",".join(
                    "?" for _ in account_ids
                )

                cursor.execute(f'''
                    SELECT
                        id,
                        name
                    FROM user_accounts
                    WHERE id IN ({placeholders})
                ''', tuple(account_ids))

                account_names = {
                    account["id"]: account["name"]
                    for account in cursor.fetchall()
                }

            finally:
                account_connection.close()

        # Attach PIC and company information to saved IDPs
        for project in projects:

            company = companies.get(
                project["company_id"]
            )

            if company is None:

                project["pic_name"] = "-"
                project["company_status"] = None
                project["pic_account_id"] = None

            else:

                project["pic_name"] = account_names.get(
                    company["account_id"],
                    "-"
                )

                project["company_status"] = company[
                    "company_status"
                ]

                project["pic_account_id"] = company[
                    "account_id"
                ]

        return projects

    # Retrieve the Customer's active saved IDPs
    def get_saved_projects(self, account_id, search_details=None):

        if search_details is None:
            search_details = {}

        search_query = search_details.get(
            "search_query",
            ""
        )

        project_type = search_details.get(
            "project_type",
            "all"
        )

        sort_by = search_details.get(
            "sort_by",
            "newest"
        )

        sort_options = {
            "newest": "s.saved_id DESC",
            "oldest": "s.saved_id ASC",
            "name_asc": (
                "p.project_name COLLATE NOCASE ASC, s.saved_id DESC"
            ),
            "name_desc": (
                "p.project_name COLLATE NOCASE DESC, s.saved_id DESC"
            )
        }

        # Sorting options are validated by the Boundary
        order_by = sort_options[sort_by]

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Suspended IDPs remain saved but are hidden from Customers
            cursor.execute(f'''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status,
                    CASE
                        WHEN c.status = 'active'
                        THEN c.category_name
                        ELSE '-'
                    END AS category_display
                FROM saved_projects AS s
                JOIN projects AS p
                    ON s.project_id = p.project_id
                LEFT JOIN idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE s.account_id = ?
                  AND p.status = 'active'
                  AND instr(
                      lower(p.project_name),
                      lower(?)
                  ) > 0
                  AND (
                      ? = 'all'
                      OR p.project_type = ?
                  )
                ORDER BY {order_by}
            ''', (
                account_id,
                search_query,
                project_type,
                project_type
            ))

            projects = [
                dict(project)
                for project in cursor.fetchall()
            ]

        finally:
            connection.close()

        # Retrieve PIC information for the saved project table
        projects = self.get_saved_project_pics(
            projects
        )

        return {
            "success": True,
            "projects": projects
        }, 200

    # Count how many Customers currently have an IDP saved
    def get_project_save_count(self, project_id):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Count saved records even when the IDP is suspended
            cursor.execute('''
                SELECT COUNT(*)
                FROM saved_projects
                WHERE project_id = ?
            ''', (project_id,))

            return cursor.fetchone()[0]

        finally:
            connection.close()
