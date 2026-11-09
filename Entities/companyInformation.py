
'''
What this code does?
- Initialise the Company Information database.
- Create company information for an Interior Designer account.
- Retrieve and view company information belonging to an account.
- Retrieve active company information for Customers.
- Update existing company information.
- Suspend or reactivate company information.
- Prevent unnecessary company status changes.
- Keep company status independent of Interior Designer projects.
- Return results through Controllers to Boundaries.
'''

import sqlite3
from pathlib import Path


class CompanyInformation:

    # Set the database file location
    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "companyInformation.db"
        )

    # Check whether an account already has company information
    def company_exists(self, account_id):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 1
                FROM company_information
                WHERE account_id = ?
                LIMIT 1
            """, (account_id,))

            return cursor.fetchone() is not None

        finally:
            connection.close()

    # Handle the Create Company Information process
    def create_company(self, company_details):

        # The UI ensures this account has no company information yet
        created = self.create_company_information(
            company_details["account_id"],
            company_details["company_name"],
            company_details["company_address"],
            company_details["working_hours"],
            company_details["company_email"],
            company_details["company_phone"],
            company_details["established_date"],
            company_details["company_description"]
        )

        if not created:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to create company information."
                },
                "status_code": 409
            }

        return {
            "data": {
                "success": True,
                "message": "Company information created successfully."
            },
            "status_code": 201
        }

    # Create company information in SQLite
    def create_company_information(
        self,
        account_id,
        company_name,
        company_address,
        working_hours,
        company_email,
        company_phone,
        established_date,
        company_description
    ):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO company_information (
                    account_id,
                    company_name,
                    company_address,
                    working_hours,
                    company_email,
                    company_phone,
                    established_date,
                    company_description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                account_id,
                company_name,
                company_address,
                working_hours,
                company_email,
                company_phone,
                established_date,
                company_description
            ))

            connection.commit()
            return True

        # Handle database constraint failures
        except sqlite3.IntegrityError:
            connection.rollback()
            return False

        finally:
            connection.close()

    # Retrieve company information belonging to an account
    def get_company_by_account_id(self, account_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    company_id,
                    account_id,
                    company_name,
                    company_address,
                    working_hours,
                    company_email,
                    company_phone,
                    established_date,
                    company_description,
                    status
                FROM company_information
                WHERE account_id = ?
            """, (account_id,))

            company = cursor.fetchone()
            return dict(company) if company else None

        finally:
            connection.close()

    # Retrieve active company information for Customers
    def get_active_company_by_company_id(self, company_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    company_id,
                    account_id,
                    company_name,
                    company_address,
                    working_hours,
                    company_email,
                    company_phone,
                    established_date,
                    company_description
                FROM company_information
                WHERE company_id = ?
                  AND status = 'active'
            """, (company_id,))

            company = cursor.fetchone()
            return dict(company) if company else None

        finally:
            connection.close()

    # Handle the View Company Information process
    def view_company(self, account_id):

        company = self.get_company_by_account_id(account_id)

        # Return None when no company information exists
        # The Boundary displays the existing empty state
        return {
            "success": True,
            "company": company
        }, 200

    # Handle the Update Company Information process
    def update_company(self, company_details):

        account_id = company_details["account_id"]

        # Check whether the company exists
        if not self.company_exists(account_id):
            return {
                "data": {
                    "success": False,
                    "message": "Company information not found."
                },
                "status_code": 404
            }

        # Update company information in the database
        updated = self.update_company_information(
            account_id,
            company_details["company_name"],
            company_details["company_address"],
            company_details["working_hours"],
            company_details["company_email"],
            company_details["company_phone"],
            company_details["established_date"],
            company_details["company_description"]
        )

        if not updated:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to update company information."
                },
                "status_code": 404
            }

        return {
            "data": {
                "success": True,
                "message": "Company information updated successfully."
            },
            "status_code": 200
        }

    # Update existing company information without changing its status
    def update_company_information(
        self,
        account_id,
        company_name,
        company_address,
        working_hours,
        company_email,
        company_phone,
        established_date,
        company_description
    ):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE company_information
                SET
                    company_name = ?,
                    company_address = ?,
                    working_hours = ?,
                    company_email = ?,
                    company_phone = ?,
                    established_date = ?,
                    company_description = ?
                WHERE account_id = ?
            """, (
                company_name,
                company_address,
                working_hours,
                company_email,
                company_phone,
                established_date,
                company_description,
                account_id
            ))

            updated = cursor.rowcount > 0
            connection.commit()
            return updated

        finally:
            connection.close()

    # Handle Suspend or Reactivate Company Information
    def change_company_status(self, status_details):

        account_id = status_details["account_id"]
        new_status = status_details["status"]

        # Retrieve the existing company information
        company = self.get_company_by_account_id(account_id)

        if company is None:
            return {
                "data": {
                    "success": False,
                    "message": "Company information not found."
                },
                "status_code": 404
            }

        # Prevent changing to the same status
        current_status = company["status"]

        if current_status == new_status:
            if new_status == "suspended":
                message = "Company information is already suspended."
            else:
                message = "Company information is already active."

            return {
                "data": {
                    "success": False,
                    "message": message
                },
                "status_code": 409
            }

        # Update company status without changing projects
        updated = self.update_company_status(
            account_id,
            new_status
        )

        if not updated:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to update company status."
                },
                "status_code": 404
            }

        if new_status == "suspended":
            message = "Company information suspended successfully."
        else:
            message = "Company information reactivated successfully."

        return {
            "data": {
                "success": True,
                "message": message
            },
            "status_code": 200
        }

    # Update company status in SQLite
    def update_company_status(self, account_id, status):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE company_information
                SET status = ?
                WHERE account_id = ?
            """, (status, account_id))

            updated = cursor.rowcount > 0
            connection.commit()
            return updated

        finally:
            connection.close()

    # Initialise the Company Information database
    def initialise_database(self):
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS company_information (
                    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL UNIQUE,
                    company_name TEXT NOT NULL,
                    company_address TEXT NOT NULL,
                    working_hours TEXT NOT NULL,
                    company_email TEXT NOT NULL,
                    company_phone TEXT NOT NULL,
                    established_date TEXT NOT NULL,
                    company_description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active'
                )
            """)

            connection.commit()

        finally:
            connection.close()
