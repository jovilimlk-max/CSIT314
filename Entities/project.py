
'''
What this code does?
- Initialise the Project database.
- Create Current IDP and Past IDP projects.
- Retrieve projects belonging to an Interior Designer's company.
- Retrieve individual projects and verify company ownership.
- Update Current IDP and Past IDP information.
- Suspend and reactivate Current IDP and Past IDP projects.
- Search projects by name using partial, case-insensitive matching.
- Return all company projects when the search query is empty.
- Store project types as 'current' or 'past'.
- Store project statuses as 'active' or 'suspended'.
- Keep company status independent of project status.
'''

import os
import sqlite3

from Entities.companyInformation import CompanyInformation


class Project:

    # Set the database file location
    def __init__(self):

        base_dir = os.path.dirname(os.path.dirname(__file__))

        self.database_path = os.path.join(
            base_dir,
            "Database",
            "project.db"
        )

        # Initialise Company Information Entity
        self.company_information = CompanyInformation()

    # Create the Project database table
    def initialise_database(self):

        os.makedirs(
            os.path.dirname(self.database_path),
            exist_ok=True
        )

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
                    status TEXT NOT NULL DEFAULT 'active'
                )
            ''')

            connection.commit()

        finally:
            connection.close()

    # Retrieve company information before creating a project
    def get_create_project_company(self, account_id):

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Company information must exist before creating a project
        if company is None:
            return {
                "success": False,
                "message": "Please create company information before creating a project."
            }, 404

        return {
            "success": True,
            "company": company
        }, 200

    # Handle the complete Create Project process
    def create_new_project(self, project_details):

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            project_details["account_id"]
        )

        # Check whether company information exists
        if company is None:
            return {
                "data": {
                    "success": False,
                    "message": "Please create company information before creating a project."
                },
                "status_code": 404
            }

        # Create the project using the existing database method
        project_id = self.create_project(
            company["company_id"],
            project_details["project_name"],
            project_details["project_description"],
            project_details["project_type"],
            project_details["start_date"],
            project_details["end_date"]
        )

        # Return an error if project creation fails
        if not project_id:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to create project."
                },
                "status_code": 500
            }

        # Return the successful creation result
        return {
            "data": {
                "success": True,
                "message": "Project created successfully.",
                "project_id": project_id
            },
            "status_code": 201
        }

    # Create a new project in SQLite
    def create_project(
        self,
        company_id,
        project_name,
        project_description,
        project_type,
        start_date,
        end_date=None
    ):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Current IDP does not have an End Date
            if project_type == "current":
                end_date = None

            cursor.execute('''
                INSERT INTO projects (
                    company_id,
                    project_name,
                    project_description,
                    start_date,
                    end_date,
                    project_type,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                company_id,
                project_name,
                project_description,
                start_date,
                end_date,
                project_type,
                "active"
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()

    # Retrieve one project using its Project ID
    def get_project_by_id(self, project_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT *
                FROM projects
                WHERE project_id = ?
            ''', (project_id,))

            project = cursor.fetchone()

            if project is None:
                return None

            return dict(project)

        finally:
            connection.close()

    # Retrieve all projects belonging to a company
    def get_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT *
                FROM projects
                WHERE company_id = ?
                ORDER BY project_id DESC
            ''', (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Retrieve Current IDP projects belonging to a company
    def get_current_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND project_type = 'current'
                ORDER BY project_id DESC
            ''', (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Retrieve Past IDP projects belonging to a company
    def get_past_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND project_type = 'past'
                ORDER BY project_id DESC
            ''', (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Handle the View Projects listing process
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

        # Retrieve all projects belonging to the company
        projects = self.get_projects_by_company_id(
            company["company_id"]
        )

        # Include current, past, active and suspended projects
        return {
            "success": True,
            "company": company,
            "projects": projects
        }, 200

    # Handle the View Individual Project process
    def view_project(self, view_details):

        # Retrieve the validated Account ID and Project ID
        account_id = view_details["account_id"]
        project_id = view_details["project_id"]

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Check whether company information exists
        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Retrieve the selected project
        project = self.get_project_by_id(project_id)

        # Check whether the project exists
        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Verify that the project belongs to the company
        if project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "Access denied. This project does not belong to your company."
            }, 403

        # Suspended projects remain accessible to their Interior Designer
        return {
            "success": True,
            "company": company,
            "project": project
        }, 200

    # Handle the complete Update Project process
    def update_project_details(self, project_details):

        # Retrieve the validated Account ID and Project ID
        account_id = project_details["account_id"]
        project_id = project_details["project_id"]

        # Retrieve company information
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Check whether company information exists
        if company is None:
            return {
                "data": {
                    "success": False,
                    "message": "Company information not found."
                },
                "status_code": 404
            }

        # Retrieve the project being updated
        project = self.get_project_by_id(project_id)

        # Check whether the project exists
        if project is None:
            return {
                "data": {
                    "success": False,
                    "message": "Project not found."
                },
                "status_code": 404
            }

        # Verify that the project belongs to the company
        if project["company_id"] != company["company_id"]:
            return {
                "data": {
                    "success": False,
                    "message": "Access denied. This project does not belong to your company."
                },
                "status_code": 403
            }

        # Update the project's information
        updated = self.update_project(
            project_id,
            project_details["project_name"],
            project_details["project_description"],
            project_details["project_type"],
            project_details["start_date"],
            project_details["end_date"]
        )

        # Return an error if updating fails
        if not updated:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to update project."
                },
                "status_code": 500
            }

        # Return the successful update result
        return {
            "data": {
                "success": True,
                "message": "Project updated successfully.",
                "project_id": project_id
            },
            "status_code": 200
        }

    # Update an existing project's information in SQLite
    def update_project(
        self,
        project_id,
        project_name,
        project_description,
        project_type,
        start_date,
        end_date=None
    ):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Current IDP must not have an End Date
            if project_type == "current":
                end_date = None

            # Do not change the project's active/suspended status
            cursor.execute('''
                UPDATE projects
                SET project_name = ?,
                    project_description = ?,
                    project_type = ?,
                    start_date = ?,
                    end_date = ?
                WHERE project_id = ?
            ''', (
                project_name,
                project_description,
                project_type,
                start_date,
                end_date,
                project_id
            ))

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    # Handle the complete Suspend/Reactivate Project process
    def change_project_status(self, status_details):

        # Retrieve the validated details
        account_id = status_details["account_id"]
        project_id = status_details["project_id"]
        requested_status = status_details["status"]

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Check whether company information exists
        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        # Retrieve the selected project
        project = self.get_project_by_id(project_id)

        # Check whether the project exists
        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        # Verify that the project belongs to the company
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

        # Update only the project's status
        updated = self.update_project_status(
            project_id,
            requested_status
        )

        # Return an error if the status update fails
        if not updated:
            return {
                "success": False,
                "message": "Unable to update project status."
            }, 500

        # Prepare the appropriate success message
        if requested_status == "suspended":
            message = "Project suspended successfully."
        else:
            message = "Project reactivated successfully."

        # Return the successful status update result
        return {
            "success": True,
            "message": message,
            "project_id": project_id,
            "status": requested_status
        }, 200

    # Update only the project's status in SQLite
    def update_project_status(self, project_id, status):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Update the project status without modifying other fields
            cursor.execute('''
                UPDATE projects
                SET status = ?
                WHERE project_id = ?
            ''', (
                status,
                project_id
            ))

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    # Handle the complete Search Projects process
    def search_projects(self, search_details):

        # Retrieve validated search details
        account_id = search_details["account_id"]
        search_query = search_details["search_query"]

        # Retrieve the Interior Designer's company
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        # Return an empty list when no company information exists
        if company is None:
            return {
                "success": True,
                "projects": []
            }, 200

        # Retrieve the company's ID
        company_id = company["company_id"]

        # Empty queries return all projects belonging to the company
        if not search_query:
            projects = self.get_projects_by_company_id(
                company_id
            )

            return {
                "success": True,
                "projects": projects
            }, 200

        # Search for matching project names in SQLite
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            # Use case-insensitive partial matching
            # instr() treats % and _ as literal characters
            # Include both project types and all project statuses
            cursor.execute('''
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND instr(
                    lower(project_name),
                    lower(?)
                ) > 0
                ORDER BY project_id DESC
            ''', (
                company_id,
                search_query
            ))

            # Convert matching database rows into dictionaries
            projects = [
                dict(project)
                for project in cursor.fetchall()
            ]

        finally:
            connection.close()

        # Return matching projects to the Controller
        return {
            "success": True,
            "projects": projects
        }, 200
