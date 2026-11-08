
'''
What this code does?
- Initialise the Project database with optional IDP categories.
- Create, view, update, suspend and search Interior Designer projects.
- Allow each project to have no category or one active category.
- Preserve existing assignments when a category is suspended.
- Return category information for Interior Designer pages.
- Keep all database operations and domain checks in the Entity.
'''

import os
import sqlite3

from Entities.companyInformation import CompanyInformation
from Entities.idpCategory import IDPCategory


class Project:

    # Set up database location and related Entities
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))

        self.database_path = os.path.join(
            base_dir,
            "Database",
            "project.db"
        )

        self.company_information = CompanyInformation()
        self.idp_category = IDPCategory()

    # Initialise category and project tables
    def initialise_database(self):

        os.makedirs(
            os.path.dirname(self.database_path),
            exist_ok=True
        )

        # Initialise categories before projects
        self.idp_category.initialise_database()

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER NOT NULL,
                    project_name TEXT NOT NULL,
                    project_description TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT,
                    project_type TEXT NOT NULL DEFAULT 'current',
                    category_id INTEGER DEFAULT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    FOREIGN KEY (category_id)
                        REFERENCES idp_categories(category_id)
                )
            ''')

            connection.commit()

        finally:
            connection.close()

    # Retrieve the Interior Designer's company for the create form
    def get_create_project_company(self, account_id):

        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Please create company information before creating a project."
            }, 404

        return {
            "success": True,
            "company": company
        }, 200

    # Create a Current or Past IDP with an optional category
    def create_new_project(self, project_details):

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            project_details["account_id"]
        )

        if company is None:
            return {
                "data": {
                    "success": False,
                    "message": "Please create company information before creating a project."
                },
                "status_code": 404
            }

        # Retrieve the optional category assignment
        category_id = project_details.get("category_id")

        # Only active categories can be newly assigned
        if not self.idp_category.is_active_category(category_id):
            return {
                "data": {
                    "success": False,
                    "message": "The selected category is unavailable."
                },
                "status_code": 400
            }

        # Current IDPs do not have an End Date
        end_date = project_details["end_date"]

        if project_details["project_type"] == "current":
            end_date = None

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Insert project details and optional category
            cursor.execute('''
                INSERT INTO projects (
                    company_id,
                    project_name,
                    project_description,
                    start_date,
                    end_date,
                    project_type,
                    category_id,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
            ''', (
                company["company_id"],
                project_details["project_name"],
                project_details["project_description"],
                project_details["start_date"],
                end_date,
                project_details["project_type"],
                category_id
            ))

            project_id = cursor.lastrowid

            connection.commit()

        finally:
            connection.close()

        if not project_id:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to create project."
                },
                "status_code": 500
            }

        return {
            "data": {
                "success": True,
                "message": "Project created successfully.",
                "project_id": project_id
            },
            "status_code": 201
        }

    # Retrieve one project together with its category information
    def get_project_by_id(self, project_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # LEFT JOIN allows projects without a category
            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status
                FROM projects AS p
                LEFT JOIN idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.project_id = ?
            ''', (project_id,))

            project = cursor.fetchone()

            return dict(project) if project else None

        finally:
            connection.close()

    # Retrieve all projects belonging to a company
    def get_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Include current, past, active and suspended projects
            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status
                FROM projects AS p
                LEFT JOIN idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.company_id = ?
                ORDER BY p.project_id DESC
            ''', (company_id,))

            return [
                dict(project)
                for project in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Retrieve Current IDPs belonging to a company
    def get_current_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status
                FROM projects AS p
                LEFT JOIN idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.company_id = ?
                  AND p.project_type = 'current'
                ORDER BY p.project_id DESC
            ''', (company_id,))

            return [
                dict(project)
                for project in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Retrieve Past IDPs belonging to a company
    def get_past_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status
                FROM projects AS p
                LEFT JOIN idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.company_id = ?
                  AND p.project_type = 'past'
                ORDER BY p.project_id DESC
            ''', (company_id,))

            return [
                dict(project)
                for project in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Handle the View Projects listing
    def view_projects(self, account_id):

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Return an empty listing if no company exists
        if company is None:
            return {
                "success": True,
                "company": None,
                "projects": []
            }, 200

        # Retrieve the company's projects
        projects = self.get_projects_by_company_id(
            company["company_id"]
        )

        return {
            "success": True,
            "company": company,
            "projects": projects
        }, 200

    # Handle the View Individual Project process
    def view_project(self, view_details):

        # Retrieve the validated details
        account_id = view_details["account_id"]
        project_id = view_details["project_id"]

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Retrieve the selected project
        project = self.get_project_by_id(project_id)

        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Verify company ownership
        if project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "Access denied. This project does not belong to your company."
            }, 403

        # Suspended projects remain visible to their Interior Designer
        return {
            "success": True,
            "company": company,
            "project": project
        }, 200

    # Update an existing Current or Past IDP
    def update_project_details(self, project_details):

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            project_details["account_id"]
        )

        if company is None:
            return {
                "data": {
                    "success": False,
                    "message": "Company information not found."
                },
                "status_code": 404
            }

        # Retrieve the project being updated
        project_id = project_details["project_id"]
        project = self.get_project_by_id(project_id)

        if project is None:
            return {
                "data": {
                    "success": False,
                    "message": "Project not found."
                },
                "status_code": 404
            }

        # Verify company ownership
        if project["company_id"] != company["company_id"]:
            return {
                "data": {
                    "success": False,
                    "message": "Access denied. This project does not belong to your company."
                },
                "status_code": 403
            }

        # Keep the existing category if the field is omitted
        # An explicitly submitted None removes the assignment
        category_id = project_details.get(
            "category_id",
            project["category_id"]
        )

        # Preserve an existing suspended category assignment
        # Only a different category must be active
        if (
            category_id != project["category_id"]
            and not self.idp_category.is_active_category(category_id)
        ):
            return {
                "data": {
                    "success": False,
                    "message": "The selected category is unavailable."
                },
                "status_code": 400
            }

        # Current IDPs do not have an End Date
        end_date = project_details["end_date"]

        if project_details["project_type"] == "current":
            end_date = None

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Update project details without changing project status
            cursor.execute('''
                UPDATE projects
                SET
                    project_name = ?,
                    project_description = ?,
                    project_type = ?,
                    start_date = ?,
                    end_date = ?,
                    category_id = ?
                WHERE project_id = ?
            ''', (
                project_details["project_name"],
                project_details["project_description"],
                project_details["project_type"],
                project_details["start_date"],
                end_date,
                category_id,
                project_id
            ))

            updated = cursor.rowcount > 0

            connection.commit()

        finally:
            connection.close()

        if not updated:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to update project."
                },
                "status_code": 500
            }

        return {
            "data": {
                "success": True,
                "message": "Project updated successfully.",
                "project_id": project_id
            },
            "status_code": 200
        }

    # Suspend or reactivate a project
    def change_project_status(self, status_details):

        # Retrieve validated status details
        account_id = status_details["account_id"]
        project_id = status_details["project_id"]
        requested_status = status_details["status"]

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Retrieve the selected project
        project = self.get_project_by_id(project_id)

        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Verify company ownership
        if project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "Access denied. This project does not belong to your company."
            }, 403

        # Prevent unnecessary status changes
        if project["status"] == requested_status:

            if requested_status == "suspended":
                message = "This project is already suspended."
            else:
                message = "This project is already active."

            return {
                "success": False,
                "message": message
            }, 400

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Only change project status
            # Do not change category or company status
            cursor.execute('''
                UPDATE projects
                SET status = ?
                WHERE project_id = ?
            ''', (
                requested_status,
                project_id
            ))

            updated = cursor.rowcount > 0

            connection.commit()

        finally:
            connection.close()

        if not updated:
            return {
                "success": False,
                "message": "Unable to update project status."
            }, 500

        # Return the appropriate message
        if requested_status == "suspended":
            message = "Project suspended successfully."
        else:
            message = "Project reactivated successfully."

        return {
            "success": True,
            "message": message,
            "project_id": project_id,
            "status": requested_status
        }, 200

    # Search projects within the Interior Designer's company
    def search_projects(self, search_details):

        # Retrieve validated search information
        account_id = search_details["account_id"]
        search_query = search_details["search_query"]

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Return an empty list if no company exists
        if company is None:
            return {
                "success": True,
                "projects": []
            }, 200

        company_id = company["company_id"]

        # Empty searches return all projects
        if not search_query:
            projects = self.get_projects_by_company_id(
                company_id
            )

            return {
                "success": True,
                "projects": projects
            }, 200

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Search using case-insensitive partial matching
            # % and _ are treated as literal characters
            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status
                FROM projects AS p
                LEFT JOIN idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.company_id = ?
                  AND instr(
                      lower(p.project_name),
                      lower(?)
                  ) > 0
                ORDER BY p.project_id DESC
            ''', (
                company_id,
                search_query
            ))

            projects = [
                dict(project)
                for project in cursor.fetchall()
            ]

        finally:
            connection.close()

        return {
            "success": True,
            "projects": projects
        }, 200
