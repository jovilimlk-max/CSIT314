
'''
What this code does?
- Initialise a separate Database/report.db for Platform Manager reports.
- Retrieve actual User Account and Project counts from their databases.
- Generate Daily Reports using actual database counts.
- Generate Weekly Reports using a simulated 7% increase.
- Generate Monthly Reports using a simulated 30% increase.
- Round simulated values up to the nearest whole number.
- Save each generated report permanently.
- Retrieve all generated reports for the Report listing.
- Retrieve an individual generated report for viewing.
- Keep all database operations and report calculations in the Entity.
'''

import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class Report:

    # Set up separate database paths
    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent / "Database"

        self.database_path = base_dir / "report.db"
        self.account_database_path = base_dir / "userAccount.db"
        self.project_database_path = base_dir / "project.db"

    # Initialise the Report database
    def initialise_database(self):

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_generated TEXT NOT NULL,
                    report_type TEXT NOT NULL
                        CHECK (report_type IN ('daily', 'weekly', 'monthly')),
                    total_user_accounts INTEGER NOT NULL,
                    total_projects INTEGER NOT NULL
                )
            """)

            connection.commit()

        finally:
            connection.close()

    # Retrieve the actual number of User Accounts
    def get_total_user_accounts(self):

        connection = sqlite3.connect(self.account_database_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM user_accounts
            """)

            return cursor.fetchone()[0]

        finally:
            connection.close()

    # Retrieve the actual number of Projects
    def get_total_projects(self):

        connection = sqlite3.connect(self.project_database_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM projects
            """)

            return cursor.fetchone()[0]

        finally:
            connection.close()

    # Calculate simulated weekly or monthly values
    def calculate_simulated_value(self, actual_count, percentage):

        # Integer arithmetic rounds up without floating-point errors
        return (
            actual_count * (100 + percentage) + 99
        ) // 100

    # Generate a Daily Report using actual database counts
    def generate_daily_report(self):

        total_user_accounts = self.get_total_user_accounts()
        total_projects = self.get_total_projects()

        return self.save_report(
            "daily",
            total_user_accounts,
            total_projects
        )

    # Generate a Weekly Report with a simulated 7% increase
    def generate_weekly_report(self):

        actual_accounts = self.get_total_user_accounts()
        actual_projects = self.get_total_projects()

        total_user_accounts = self.calculate_simulated_value(
            actual_accounts,
            7
        )

        total_projects = self.calculate_simulated_value(
            actual_projects,
            7
        )

        return self.save_report(
            "weekly",
            total_user_accounts,
            total_projects
        )

    # Generate a Monthly Report with a simulated 30% increase
    def generate_monthly_report(self):

        actual_accounts = self.get_total_user_accounts()
        actual_projects = self.get_total_projects()

        total_user_accounts = self.calculate_simulated_value(
            actual_accounts,
            30
        )

        total_projects = self.calculate_simulated_value(
            actual_projects,
            30
        )

        return self.save_report(
            "monthly",
            total_user_accounts,
            total_projects
        )

    # Save generated report information permanently
    def save_report(
        self,
        report_type,
        total_user_accounts,
        total_projects
    ):

        # Record the generation time in Singapore time
        date_generated = datetime.now(
            ZoneInfo("Asia/Singapore")
        ).strftime("%Y-%m-%d %H:%M:%S")

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO reports (
                    date_generated,
                    report_type,
                    total_user_accounts,
                    total_projects
                )
                VALUES (?, ?, ?, ?)
            """, (
                date_generated,
                report_type,
                total_user_accounts,
                total_projects
            ))

            report_id = cursor.lastrowid

            connection.commit()

            return {
                "success": True,
                "message": (
                    report_type.capitalize()
                    + " report generated successfully."
                ),
                "report_id": report_id
            }, 201

        finally:
            connection.close()

    # Retrieve all generated reports for the Report table
    def get_all_reports(self):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    report_id,
                    date_generated,
                    report_type,
                    total_user_accounts,
                    total_projects
                FROM reports
                ORDER BY report_id DESC
            """)

            return [
                dict(report)
                for report in cursor.fetchall()
            ]

        finally:
            connection.close()

    # Retrieve a single report for the View Report page
    def get_report_by_id(self, report_id):

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    report_id,
                    date_generated,
                    report_type,
                    total_user_accounts,
                    total_projects
                FROM reports
                WHERE report_id = ?
            """, (report_id,))

            report = cursor.fetchone()

            return dict(report) if report else None

        finally:
            connection.close()
