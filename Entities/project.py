
'''
What this code does?
- Initialise the Project database.
- Create new projects linked to a company.
- Retrieve an individual project using its Project ID.
- Retrieve all projects belonging to a company.
- Retrieve ongoing and completed projects separately.
- Update existing project information.
- Preserve the project's company association and status.
'''

import sqlite3
import os


class Project:

    # Set the database file location
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))

        self.database_path = os.path.join(
            base_dir,
            "Database",
            "project.db"
        )

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
                    progress TEXT NOT NULL DEFAULT 'Ongoing',
                    status TEXT NOT NULL DEFAULT 'active'
                )
            ''')

            connection.commit()

        finally:
            connection.close()

    # Create a new project
    def create_project(self, company_id, project_name,
                       project_description, progress, start_date,
                       end_date=None):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Ongoing projects do not have an End Date
            if progress == "Ongoing":
                end_date = None

            cursor.execute('''
                INSERT INTO projects (
                    company_id,
                    project_name,
                    project_description,
                    start_date,
                    end_date,
                    progress,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                company_id,
                project_name,
                project_description,
                start_date,
                end_date,
                progress,
                "active"
            ))

            connection.commit()

            # Return the ID of the newly created project
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

    # Retrieve ongoing projects belonging to a company
    def get_current_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND progress = 'Ongoing'
                ORDER BY project_id DESC
            ''', (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Retrieve completed projects belonging to a company
    def get_past_projects_by_company_id(self, company_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND progress = 'Completed'
                ORDER BY project_id DESC
            ''', (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Update an existing project's information
    def update_project(self, project_id, project_name,
                       project_description, progress, start_date,
                       end_date=None):

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            # Ongoing projects must not have an End Date
            if progress == "Ongoing":
                end_date = None

            # Update project details without changing company_id or status
            cursor.execute('''
                UPDATE projects
                SET project_name = ?,
                    project_description = ?,
                    progress = ?,
                    start_date = ?,
                    end_date = ?
                WHERE project_id = ?
            ''', (
                project_name,
                project_description,
                progress,
                start_date,
                end_date,
                project_id
            ))

            connection.commit()

            # Return True if a project record was found and updated
            return cursor.rowcount > 0

        finally:
            connection.close()
