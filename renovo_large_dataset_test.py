
"""What this code does?
Creates an isolated copy of Renovo's six SQLite databases, adds synthetic
test records, and checks searching, filtering and pagination.

Your original databases are not modified.
"""

import argparse
import hashlib
import shutil
import sqlite3
import time
from datetime import date, timedelta
from pathlib import Path


DATABASES = [
    "userAccount.db",
    "userProfile.db",
    "companyInformation.db",
    "project.db",
    "idpCategory.db",
    "report.db",
]


def open_db(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database-dir",
        type=Path,
        default=Path("Database")
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("large_dataset_evidence")
    )
    args = parser.parse_args()

    source = args.database_dir.resolve()
    destination = args.output_dir.resolve()

    # Prevent output from replacing the original database folder.
    if destination == source or destination in source.parents:
        raise SystemExit("Choose a separate output folder.")

    if destination.exists():
        raise SystemExit(
            f"Output folder already exists: {destination}. "
            "Choose another output folder."
        )

    # Check that all six source databases exist.
    for name in DATABASES:
        if not (source / name).is_file():
            raise SystemExit(f"Missing database: {source / name}")

    # Copy databases into an isolated testing folder.
    destination.mkdir(parents=True)

    for name in DATABASES:
        shutil.copy2(source / name, destination / name)

    dbs = {
        name: open_db(destination / name)
        for name in DATABASES
    }

    suffix = "LDT20261112"

    # Generate a test password hash.
    salt = "renovoloadtest"
    password_hash = (
        "pbkdf2:sha256:600000$"
        + salt
        + "$"
        + hashlib.pbkdf2_hmac(
            "sha256",
            b"TestOnly-12345",
            salt.encode(),
            600000
        ).hex()
    )

    try:
        profiles = dbs["userProfile.db"]
        accounts = dbs["userAccount.db"]
        companies = dbs["companyInformation.db"]
        projects = dbs["project.db"]
        categories = dbs["idpCategory.db"]
        reports = dbs["report.db"]

        # 1. Generate 100 user profiles.
        with profiles:
            for n in range(1, 101):
                profiles.execute(
                    """
                    INSERT INTO user_profiles
                    (profile_name, description, status)
                    VALUES (?, ?, ?)
                    """,
                    (
                        f"Load Profile {suffix} {n:03}",
                        f"Synthetic profile {n}",
                        "active" if n % 5 else "suspended"
                    )
                )

        # 2. Generate 100 IDP categories.
        with categories:
            for n in range(1, 101):
                categories.execute(
                    """
                    INSERT INTO idp_categories
                    (category_name, category_description, status)
                    VALUES (?, ?, ?)
                    """,
                    (
                        f"Load Category {suffix} {n:03}",
                        f"Synthetic category {n}",
                        "active" if n % 5 else "suspended"
                    )
                )

        active_categories = [
            row["category_id"]
            for row in categories.execute(
                """
                SELECT category_id
                FROM idp_categories
                WHERE category_name LIKE ?
                AND status = ?
                ORDER BY category_id
                """,
                (f"Load Category {suffix} %", "active")
            )
        ]

        # 3. Generate 200 accounts: 100 designers and 100 customers.
        with accounts:
            for n in range(1, 101):
                for kind, role in [
                    ("designer", "interior_designer"),
                    ("customer", "customer")
                ]:
                    accounts.execute(
                        """
                        INSERT INTO user_accounts
                        (name, email, password_hash, role, status)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            f"Load {kind} {n:03}",
                            f"{kind}.{suffix.lower()}.{n:03}@example.invalid",
                            password_hash,
                            role,
                            "suspended" if n % 10 == 0 else "active"
                        )
                    )

        designers = [
            row["id"]
            for row in accounts.execute(
                """
                SELECT id FROM user_accounts
                WHERE email LIKE ?
                ORDER BY id
                """,
                (f"designer.{suffix.lower()}.%@example.invalid",)
            )
        ]

        customers = [
            row["id"]
            for row in accounts.execute(
                """
                SELECT id FROM user_accounts
                WHERE email LIKE ?
                ORDER BY id
                """,
                (f"customer.{suffix.lower()}.%@example.invalid",)
            )
        ]

        # 4. Generate 100 company information records.
        with companies:
            for n, account_id in enumerate(designers, 1):
                companies.execute(
                    """
                    INSERT INTO company_information
                    (
                        account_id, company_name, company_address,
                        working_hours, company_email, company_phone,
                        established_date, company_description, status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        account_id,
                        f"Load Company {suffix} {n:03}",
                        f"{n} Test Road Singapore",
                        "09:00-18:00",
                        f"company.{suffix.lower()}.{n:03}@example.invalid",
                        f"6000{n:04}",
                        "2020-01-01",
                        "Synthetic company for load testing",
                        "active" if n % 5 else "suspended"
                    )
                )

        company_ids = [
            row["company_id"]
            for row in companies.execute(
                """
                SELECT company_id FROM company_information
                WHERE company_name LIKE ?
                ORDER BY company_id
                """,
                (f"Load Company {suffix} %",)
            )
        ]

        # 5. Generate projects, view counts and saved projects.
        project_ids = []

        with projects:
            for n, company_id in enumerate(company_ids, 1):
                project_type = "current" if n % 2 else "past"
                start_date = f"2026-01-{(n % 28) + 1:02d}"
                end_date = (
                    None if project_type == "current"
                    else "2026-10-01"
                )

                cursor = projects.execute(
                    """
                    INSERT INTO projects
                    (
                        company_id, project_name, project_description,
                        start_date, end_date, project_type,
                        category_id, status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        company_id,
                        f"Load Project {suffix} {n:03}",
                        f"Synthetic project {n}",
                        start_date,
                        end_date,
                        project_type,
                        active_categories[
                            (n - 1) % len(active_categories)
                        ],
                        "active" if n % 5 else "suspended"
                    )
                )

                project_id = cursor.lastrowid
                project_ids.append(project_id)

                projects.execute(
                    """
                    INSERT INTO project_views (project_id, view_count)
                    VALUES (?, ?)
                    """,
                    (project_id, n)
                )

            for account_id, project_id in zip(
                customers, project_ids
            ):
                projects.execute(
                    """
                    INSERT INTO saved_projects
                    (account_id, project_id)
                    VALUES (?, ?)
                    """,
                    (account_id, project_id)
                )

        # 6. Generate 100 report records.
        with reports:
            for n in range(1, 101):
                report_date = (
                    date(2026, 1, 1) + timedelta(days=n - 1)
                ).isoformat()

                report_type = [
                    "daily", "weekly", "monthly"
                ][(n - 1) % 3]

                reports.execute(
                    """
                    INSERT INTO reports
                    (
                        date_generated, report_type,
                        total_user_accounts, total_projects
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        report_date,
                        report_type,
                        200 + n,
                        100 + n
                    )
                )

        # 7. Count the records in each table.
        tables = {
            "User profiles": (profiles, "user_profiles"),
            "User accounts": (accounts, "user_accounts"),
            "Company information": (
                companies, "company_information"
            ),
            "IDP categories": (categories, "idp_categories"),
            "Projects": (projects, "projects"),
            "Project views": (projects, "project_views"),
            "Saved projects": (projects, "saved_projects"),
            "Reports": (reports, "reports")
        }

        lines = [
            "RENOVO LARGE DATASET TEST",
            "Isolated database copies",
            f"Output folder: {destination}",
            "",
            "DATABASE COUNTS"
        ]

        for label, (db, table) in tables.items():
            count = db.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            lines.append(f"{label}: {count} total records")

        # 8. Run representative database checks.
        checks = [
            (
                "Profile search",
                profiles,
                "SELECT COUNT(*) FROM user_profiles "
                "WHERE profile_name LIKE ?",
                (f"Load Profile {suffix} %",),
                100
            ),
            (
                "Account search",
                accounts,
                "SELECT COUNT(*) FROM user_accounts "
                "WHERE email LIKE ?",
                (f"customer.{suffix.lower()}.%@example.invalid",),
                100
            ),
            (
                "Account status filter",
                accounts,
                "SELECT COUNT(*) FROM user_accounts "
                "WHERE email LIKE ? AND status = 'suspended'",
                (f"customer.{suffix.lower()}.%@example.invalid",),
                10
            ),
            (
                "Company search",
                companies,
                "SELECT COUNT(*) FROM company_information "
                "WHERE company_name LIKE ?",
                (f"Load Company {suffix} %",),
                100
            ),
            (
                "Project search",
                projects,
                "SELECT COUNT(*) FROM projects "
                "WHERE project_name LIKE ?",
                (f"Load Project {suffix} %",),
                100
            ),
            (
                "Current project filter",
                projects,
                "SELECT COUNT(*) FROM projects "
                "WHERE project_name LIKE ? "
                "AND project_type = 'current'",
                (f"Load Project {suffix} %",),
                50
            ),
            (
                "Past project filter",
                projects,
                "SELECT COUNT(*) FROM projects "
                "WHERE project_name LIKE ? "
                "AND project_type = 'past'",
                (f"Load Project {suffix} %",),
                50
            ),
            (
                "Category search",
                categories,
                "SELECT COUNT(*) FROM idp_categories "
                "WHERE category_name LIKE ?",
                (f"Load Category {suffix} %",),
                100
            ),
            (
                "Saved project search",
                projects,
                "SELECT COUNT(*) FROM saved_projects sp "
                "JOIN projects p ON sp.project_id = p.project_id "
                "WHERE p.project_name LIKE ?",
                (f"Load Project {suffix} %",),
                100
            ),
            (
                "View count retrieval",
                projects,
                "SELECT COUNT(*) FROM project_views pv "
                "JOIN projects p ON pv.project_id = p.project_id "
                "WHERE p.project_name LIKE ?",
                (f"Load Project {suffix} %",),
                100
            ),
            (
                "Report listing",
                reports,
                "SELECT COUNT(*) FROM reports "
                "WHERE total_user_accounts BETWEEN 201 AND 300",
                (),
                100
            ),
            (
                "Account pagination (5 rows)",
                accounts,
                "SELECT COUNT(*) FROM "
                "(SELECT id FROM user_accounts "
                "WHERE email LIKE ? "
                "ORDER BY id LIMIT 5 OFFSET 5)",
                (f"customer.{suffix.lower()}.%@example.invalid",),
                5
            )
        ]

        lines.extend([
            "",
            "DATABASE QUERY CHECKS",
            "(Single-run timings, not performance benchmarks)"
        ])

        passed = 0

        for name, db, sql, params, expected in checks:
            start = time.perf_counter()

            actual = db.execute(
                sql, params
            ).fetchone()[0]

            elapsed_ms = (
                time.perf_counter() - start
            ) * 1000

            success = actual == expected

            if success:
                passed += 1

            status = "PASS" if success else "FAIL"

            lines.append(
                f"{status} | {name} | "
                f"found {actual}, expected {expected} | "
                f"{elapsed_ms:.3f} ms"
            )

        lines.extend([
            "",
            f"RESULT: {passed}/{len(checks)} checks passed.",
            "Scope: SQLite database checks, not Flask UI tests.",
            "All synthetic records were written to database copies."
        ])

        # Save results to a text file for report evidence.
        result_text = "\n".join(lines) + "\n"

        (destination / "test_results.txt").write_text(
            result_text,
            encoding="utf-8"
        )

        print(result_text)

        if passed != len(checks):
            raise SystemExit("Some database checks failed.")

    finally:
        for db in dbs.values():
            db.close()


if __name__ == "__main__":
    main()
