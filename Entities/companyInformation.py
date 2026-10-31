
'''
What this code does?
- Handle company information and interact with the database.
- Create company information for an Interior Designer account.
- Check whether an account already has company information.
- Retrieve company information belonging to an account.
- Update existing company information.
- Allow one company information record per account.
- Store company status as active when created.
- Initialise the company information database.
'''

import sqlite3
from pathlib import Path


class CompanyInformation:

    def __init__(self):
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "Database"
            / "companyInformation.db"
        )

    # Check whether the account already has company information
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

    # Create company information for an Interior Designer account
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

    # Update the existing company information
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

            # Check whether the company record exists
            updated = cursor.rowcount > 0

            connection.commit()

            return updated

        finally:
            connection.close()

    # Initialise the company information database
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
