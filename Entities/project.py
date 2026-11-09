
'''
What this code does?
- Initialise and manage Interior Designer Projects.
- Create, view, update, suspend and search Current and Past IDPs.
- Store projects in Database/project.db.
- Retrieve IDP categories from the separate Database/idpCategory.db.
- Preserve optional category assignments when categories are suspended.
- Retrieve active Customer IDPs with their category and PIC.
- Record Customer views and retrieve view and saved counts.
- Allow project details to be retrieved without recording another view.
- Retrieve active company information associated with a Customer IDP.
- Keep suspended projects hidden from Customers.
- Keep database operations and domain checks in the Entity.
'''

import os
import sqlite3

from Entities.companyInformation import CompanyInformation
from Entities.idpCategory import IDPCategory
from Entities.savedProject import SavedProject


class Project:

    # Set up the database paths and related Entities
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))

        self.database_path = os.path.join(
            base_dir, "Database", "project.db"
        )

        self.category_database_path = os.path.join(
            base_dir, "Database", "idpCategory.db"
        )

        self.company_database_path = os.path.join(
            base_dir, "Database", "companyInformation.db"
        )

        self.account_database_path = os.path.join(
            base_dir, "Database", "userAccount.db"
        )

        self.company_information = CompanyInformation()
        self.idp_category = IDPCategory()
        self.saved_project = SavedProject()

    # Attach the separate category database to a project connection
    def attach_category_database(self, connection):
        connection.execute(
            "ATTACH DATABASE ? AS category_db",
            (self.category_database_path,)
        )

    # Initialise project and view-count tables
    def initialise_database(self):
        os.makedirs(
            os.path.dirname(self.database_path),
            exist_ok=True
        )

        # Categories are initialised in their own database
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
                    status TEXT NOT NULL DEFAULT 'active'
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_views (
                    project_id INTEGER PRIMARY KEY,
                    view_count INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (project_id)
                        REFERENCES projects(project_id)
                )
            ''')

            connection.commit()

        finally:
            connection.close()

        self.saved_project.initialise_database()

    # Retrieve the Interior Designer's company before creating a project
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

    # Create a Current or Past IDP
    def create_new_project(self, project_details):
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

        category_id = project_details.get("category_id")

        # Check the category using the separate category Entity
        if not self.idp_category.is_active_category(category_id):
            return {
                "data": {
                    "success": False,
                    "message": "The selected category is unavailable."
                },
                "status_code": 400
            }

        end_date = project_details.get("end_date")

        if project_details["project_type"] == "current":
            end_date = None

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

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

        return {
            "data": {
                "success": True,
                "message": "Project created successfully.",
                "project_id": project_id
            },
            "status_code": 201
        }

    # Retrieve a project with its category and engagement counts
    def get_project_by_id(self, project_id):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            self.attach_category_database(connection)
            cursor = connection.cursor()

            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status,
                    COALESCE(v.view_count, 0) AS view_count,
                    (
                        SELECT COUNT(*)
                        FROM saved_projects AS s
                        WHERE s.project_id = p.project_id
                    ) AS save_count
                FROM projects AS p
                LEFT JOIN category_db.idp_categories AS c
                    ON p.category_id = c.category_id
                LEFT JOIN project_views AS v
                    ON p.project_id = v.project_id
                WHERE p.project_id = ?
            ''', (project_id,))

            project = cursor.fetchone()
            return dict(project) if project else None

        finally:
            connection.close()

    # Retrieve projects belonging to an Interior Designer company
    def get_projects_by_company_id(self, company_id):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            self.attach_category_database(connection)
            cursor = connection.cursor()

            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status,
                    COALESCE(v.view_count, 0) AS view_count,
                    (
                        SELECT COUNT(*)
                        FROM saved_projects AS s
                        WHERE s.project_id = p.project_id
                    ) AS save_count
                FROM projects AS p
                LEFT JOIN category_db.idp_categories AS c
                    ON p.category_id = c.category_id
                LEFT JOIN project_views AS v
                    ON p.project_id = v.project_id
                WHERE p.company_id = ?
                ORDER BY p.project_id DESC
            ''', (company_id,))

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Retrieve Current IDPs
    def get_current_projects_by_company_id(self, company_id):
        return [
            project
            for project in self.get_projects_by_company_id(company_id)
            if project["project_type"] == "current"
        ]

    # Retrieve Past IDPs
    def get_past_projects_by_company_id(self, company_id):
        return [
            project
            for project in self.get_projects_by_company_id(company_id)
            if project["project_type"] == "past"
        ]

    # Retrieve Interior Designer project listing
    def view_projects(self, account_id):
        company = self.company_information.get_company_by_account_id(
            account_id
        )

        if company is None:
            return {
                "success": True,
                "company": None,
                "projects": []
            }, 200

        projects = self.get_projects_by_company_id(
            company["company_id"]
        )

        return {
            "success": True,
            "company": company,
            "projects": projects
        }, 200

    # View an Interior Designer project without increasing its view count
    def view_project(self, view_details):
        company = self.company_information.get_company_by_account_id(
            view_details["account_id"]
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        project = self.get_project_by_id(
            view_details["project_id"]
        )

        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        if project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "Access denied. This project does not belong to your company."
            }, 403

        return {
            "success": True,
            "company": company,
            "project": project
        }, 200

    # Update an Interior Designer project
    def update_project_details(self, project_details):
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

        if project["company_id"] != company["company_id"]:
            return {
                "data": {
                    "success": False,
                    "message": "Access denied."
                },
                "status_code": 403
            }

        category_id = project_details.get(
            "category_id",
            project["category_id"]
        )

        # Existing assignments may remain even if a category is suspended.
        # New assignments must use active categories.
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

        end_date = project_details.get("end_date")

        if project_details["project_type"] == "current":
            end_date = None

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

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

        return {
            "data": {
                "success": updated,
                "message": (
                    "Project updated successfully."
                    if updated
                    else "Unable to update project."
                ),
                "project_id": project_id
            },
            "status_code": 200 if updated else 500
        }

    # Suspend or reactivate an Interior Designer project
    def change_project_status(self, status_details):
        company = self.company_information.get_company_by_account_id(
            status_details["account_id"]
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information not found."
            }, 404

        project_id = status_details["project_id"]
        requested_status = status_details["status"]

        if requested_status not in ("active", "suspended"):
            return {
                "success": False,
                "message": "Invalid project status."
            }, 400

        project = self.get_project_by_id(project_id)

        if project is None:
            return {
                "success": False,
                "message": "Project not found."
            }, 404

        if project["company_id"] != company["company_id"]:
            return {
                "success": False,
                "message": "Access denied."
            }, 403

        if project["status"] == requested_status:
            return {
                "success": False,
                "message": "Project is already " + requested_status + "."
            }, 400

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute('''
                UPDATE projects
                SET status = ?
                WHERE project_id = ?
            ''', (
                requested_status,
                project_id
            ))

            connection.commit()

        finally:
            connection.close()

        return {
            "success": True,
            "message": "Project status updated successfully.",
            "project_id": project_id,
            "status": requested_status
        }, 200

    # Search an Interior Designer's projects by name
    def search_projects(self, search_details):
        company = self.company_information.get_company_by_account_id(
            search_details["account_id"]
        )

        if company is None:
            return {
                "success": True,
                "projects": []
            }, 200

        projects = self.get_projects_by_company_id(
            company["company_id"]
        )

        query = search_details["search_query"].lower()

        matching_projects = [
            project
            for project in projects
            if query in project["project_name"].lower()
        ]

        return {
            "success": True,
            "projects": matching_projects
        }, 200

    # Retrieve active categories for the Customer category dropdown
    def get_customer_categories(self):

        # IDPCategory handles access to idpCategory.db
        return self.idp_category.get_active_categories()

    # Attach PIC names and company status to project records
    def get_customer_project_pics(self, projects):
        if not projects:
            return projects

        company_ids = {
            project["company_id"]
            for project in projects
        }

        placeholders = ",".join(
            "?" for _ in company_ids
        )

        connection = sqlite3.connect(
            self.company_database_path
        )
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute(f'''
                SELECT
                    company_id,
                    account_id,
                    status AS company_status
                FROM company_information
                WHERE company_id IN ({placeholders})
            ''', tuple(company_ids))

            companies = {
                row["company_id"]: dict(row)
                for row in cursor.fetchall()
            }

        finally:
            connection.close()

        account_ids = {
            company["account_id"]
            for company in companies.values()
        }

        account_names = {}

        if account_ids:
            placeholders = ",".join(
                "?" for _ in account_ids
            )

            connection = sqlite3.connect(
                self.account_database_path
            )
            connection.row_factory = sqlite3.Row

            try:
                cursor = connection.cursor()

                cursor.execute(f'''
                    SELECT id, name
                    FROM user_accounts
                    WHERE id IN ({placeholders})
                ''', tuple(account_ids))

                account_names = {
                    row["id"]: row["name"]
                    for row in cursor.fetchall()
                }

            finally:
                connection.close()

        for project in projects:
            company = companies.get(
                project["company_id"]
            )

            if company is None:
                project["pic_name"] = "-"
                project["pic_account_id"] = None
                project["company_status"] = None

            else:
                project["pic_name"] = account_names.get(
                    company["account_id"],
                    "-"
                )

                project["pic_account_id"] = company["account_id"]
                project["company_status"] = company["company_status"]

        return projects

    # Retrieve active Customer IDPs
    def search_customer_projects(self, search_details=None):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            self.attach_category_database(connection)
            cursor = connection.cursor()

            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status,
                    CASE
                        WHEN c.status = 'active'
                        THEN c.category_name
                        ELSE '-'
                    END AS category_display
                FROM projects AS p
                LEFT JOIN category_db.idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.status = 'active'
                ORDER BY p.project_id DESC
            ''')

            projects = [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

        # Add Interior Designer PIC and company status
        projects = self.get_customer_project_pics(
            projects
        )

        categories = self.get_customer_categories()

        return {
            "success": True,
            "projects": projects,
            "categories": categories
        }, 200

    # Retrieve an active Customer IDP and optionally record a view
    def view_customer_project(self, project_id, count_view=True):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            self.attach_category_database(connection)
            cursor = connection.cursor()

            # Customers can open active IDPs only
            cursor.execute('''
                SELECT
                    p.*,
                    c.category_name,
                    c.status AS category_status,
                    CASE
                        WHEN c.status = 'active'
                        THEN c.category_name
                        ELSE '-'
                    END AS category_display,
                    (
                        SELECT COUNT(*)
                        FROM saved_projects AS s
                        WHERE s.project_id = p.project_id
                    ) AS save_count
                FROM projects AS p
                LEFT JOIN category_db.idp_categories AS c
                    ON p.category_id = c.category_id
                WHERE p.project_id = ?
                  AND p.status = 'active'
            ''', (project_id,))

            project = cursor.fetchone()

            if project is None:
                return {
                    "success": False,
                    "message": "Project not found or unavailable."
                }, 404

            project_details = dict(project)

            # Increase view count only for a normal Customer view
            if count_view:
                cursor.execute('''
                    INSERT INTO project_views (
                        project_id,
                        view_count
                    )
                    VALUES (?, 1)
                    ON CONFLICT(project_id)
                    DO UPDATE SET
                        view_count = view_count + 1
                ''', (project_id,))

                connection.commit()

            # Retrieve the latest view count
            cursor.execute('''
                SELECT view_count
                FROM project_views
                WHERE project_id = ?
            ''', (project_id,))

            view_record = cursor.fetchone()

            project_details["view_count"] = (
                view_record["view_count"]
                if view_record
                else 0
            )

        finally:
            connection.close()

        # Attach Interior Designer PIC and company status
        project_details = self.get_customer_project_pics(
            [project_details]
        )[0]

        return {
            "success": True,
            "project": project_details
        }, 200

    # Retrieve active company information linked to an active Customer IDP
    def get_customer_project_company_information(self, project_id):

        # Retrieve the project without recording another view
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT
                    project_id,
                    company_id
                FROM projects
                WHERE project_id = ?
                  AND status = 'active'
            ''', (project_id,))

            project = cursor.fetchone()

        finally:
            connection.close()

        if project is None:
            return {
                "success": False,
                "message": "Project not found or unavailable."
            }, 404

        # Suspended company information is hidden from Customers
        company = self.company_information.get_active_company_by_company_id(
            project["company_id"]
        )

        if company is None:
            return {
                "success": False,
                "message": "Company information is unavailable."
            }, 404

        return {
            "success": True,
            "company": company,
            "project_id": project_id
        }, 200
