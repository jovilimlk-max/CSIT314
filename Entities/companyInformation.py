
'''
What this code does?
- Initialise the Company Information database.
- Create company information for an Interior Designer account.
- Retrieve and view company information belonging to an account.
- Update existing company information.
- Suspend or reactivate company information.
- Prevent unnecessary company status changes.
- Keep company status independent of Interior Designer projects.
- Handle database operations and domain checks within the Entity.
- Avoid unnecessary methods that duplicate the same operation.
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

    # Create company information in the database
    def create_company(self, company_details):

        # The UI ensures that the account has no company information yet
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Insert the validated company details
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
                company_details["account_id"],
                company_details["company_name"],
                company_details["company_address"],
                company_details["working_hours"],
                company_details["company_email"],
                company_details["company_phone"],
                company_details["established_date"],
                company_details["company_description"]
            ))

            connection.commit()

            # Return the successful creation result
            return {
                "data": {
                    "success": True,
                    "message": "Company information created successfully."
                },
                "status_code": 201
            }

        # Handle database constraint failures
        except sqlite3.IntegrityError:
            connection.rollback()

            return {
                "data": {
                    "success": False,
                    "message": "Unable to create company information."
                },
                "status_code": 409
            }

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

    # Handle the View Company Information process
    def view_company(self, account_id):

        # Retrieve company information for the account
        company = self.get_company_by_account_id(account_id)

        # Return None when no company information exists
        # The Boundary handles the empty state
        return {
            "success": True,
            "company": company
        }, 200

    # Update existing company information
    def update_company(self, company_details):

        # Retrieve the Account ID
        account_id = company_details["account_id"]

        # Check whether company information exists
        if not self.company_exists(account_id):
            return {
                "data": {
                    "success": False,
                    "message": "Company information not found."
                },
                "status_code": 404
            }

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Update company information without changing its status
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
                company_details["company_name"],
                company_details["company_address"],
                company_details["working_hours"],
                company_details["company_email"],
                company_details["company_phone"],
                company_details["established_date"],
                company_details["company_description"],
                account_id
            ))

            updated = cursor.rowcount > 0

            connection.commit()

            # Return an error if no company record was updated
            if not updated:
                return {
                    "data": {
                        "success": False,
                        "message": "Unable to update company information."
                    },
                    "status_code": 404
                }

            # Return the successful update result
            return {
                "data": {
                    "success": True,
                    "message": "Company information updated successfully."
                },
                "status_code": 200
            }

        finally:
            connection.close()

    # Suspend or reactivate company information
    def change_company_status(self, status_details):

        # Retrieve the validated Account ID and requested status
        account_id = status_details["account_id"]
        new_status = status_details["status"]

        # Retrieve the existing company information
        company = self.get_company_by_account_id(account_id)

        # Return an error when company information does not exist
        if company is None:
            return {
                "data": {
                    "success": False,
                    "message": "Company information not found."
                },
                "status_code": 404
            }

        # Retrieve the current company status
        current_status = company["status"]

        # Prevent changing to the same status
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

        # Update company status directly in the database
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE company_information
                SET status = ?
                WHERE account_id = ?
            """, (
                new_status,
                account_id
            ))

            updated = cursor.rowcount > 0

            connection.commit()

        finally:
            connection.close()

        # Return an error if the update was unsuccessful
        if not updated:
            return {
                "data": {
                    "success": False,
                    "message": "Unable to update company status."
                },
                "status_code": 404
            }

        # Return the appropriate success message
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

    # Initialise the Company Information database
    def initialise_database(self):

        # Create the Database folder if it does not exist
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()

            # Create the company information table
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
