
'''
What this code does?
- Create and initialise the Project database.
- Store projects linked to a company.
- Create new Ongoing or Completed projects.
- Retrieve a specific project by its ID.
- Retrieve all projects belonging to a company.
- Retrieve Ongoing projects belonging to a company.
- Retrieve Completed projects belonging to a company.
'''

import os
import sqlite3


class Project:

    def __init__(self):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        database_dir = os.path.join(base_dir, "Database")
        os.makedirs(database_dir, exist_ok=True)

        self.db_path = os.path.join(
            database_dir,
            "project.db"
        )

    # Initialise the Project database
    def initialise_database(self):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
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
            """)

            connection.commit()

        finally:
            connection.close()

    # Create a new project
    def create_project(
        self,
        company_id,
        project_name,
        project_description,
        progress,
        start_date,
        end_date=None
    ):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
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
            """, (
                company_id,
                project_name,
                project_description,
                start_date,
                end_date if progress == "Completed" else None,
                progress,
                "active"
            ))

            project_id = cursor.lastrowid

            connection.commit()

            return project_id

        finally:
            connection.close()

    # Retrieve a specific project by its ID
    def get_project_by_id(self, project_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM projects
                WHERE project_id = ?
            """, (project_id,))

            project = cursor.fetchone()

            if project is None:
                return None

            return dict(project)

        finally:
            connection.close()

    # Retrieve all projects belonging to a company
    def get_projects_by_company_id(self, company_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM projects
                WHERE company_id = ?
                ORDER BY project_id DESC
            """, (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Retrieve Ongoing projects belonging to a company
    def get_current_projects_by_company_id(self, company_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND progress = 'Ongoing'
                ORDER BY project_id DESC
            """, (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()

    # Retrieve Completed projects belonging to a company
    def get_past_projects_by_company_id(self, company_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM projects
                WHERE company_id = ?
                AND progress = 'Completed'
                ORDER BY project_id DESC
            """, (company_id,))

            projects = cursor.fetchall()

            return [dict(project) for project in projects]

        finally:
            connection.close()
