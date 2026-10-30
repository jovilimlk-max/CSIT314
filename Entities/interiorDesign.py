"""Persist designer-owned company information and projects."""
import sqlite3
from contextlib import contextmanager


class InteriorDesign:
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys = ON')
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialise_database(self):
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS designer_companies (
                    id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL UNIQUE
                    REFERENCES user_accounts(id), name TEXT NOT NULL,
                    address TEXT NOT NULL, hours TEXT NOT NULL, email TEXT NOT NULL,
                    phone TEXT NOT NULL, established TEXT NOT NULL,
                    description TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active'
                );
                CREATE TABLE IF NOT EXISTS design_projects (
                    id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL
                    REFERENCES designer_companies(id), name TEXT NOT NULL,
                    description TEXT NOT NULL, progress TEXT NOT NULL,
                    start_date TEXT NOT NULL, end_date TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            ''')

    def company(self, owner_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM designer_companies WHERE owner_id=?', (owner_id,)).fetchone()
            return dict(row) if row else None

    def save_company(self, owner_id, values):
        with self.connect() as db:
            db.execute('''INSERT INTO designer_companies
                (owner_id,name,address,hours,email,phone,established,description)
                VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(owner_id) DO UPDATE SET
                name=excluded.name,address=excluded.address,hours=excluded.hours,
                email=excluded.email,phone=excluded.phone,
                established=excluded.established,description=excluded.description''',
                (owner_id, *(values[key] for key in ('name','address','hours','email','phone','established','description'))))

    def designers(self, owner_id):
        # There is no company membership model in the existing account schema.
        # Only the verified company owner can be listed as a member.
        with self.connect() as db:
            return [dict(row) for row in db.execute(
                'SELECT name,email,status FROM user_accounts WHERE id=? AND role=?',
                (owner_id, 'designer'))]

    def projects(self, company_id):
        with self.connect() as db:
            return [dict(row) for row in db.execute(
                'SELECT * FROM design_projects WHERE company_id=? ORDER BY id DESC', (company_id,))]

    def project(self, company_id, project_id):
        return next((p for p in self.projects(company_id) if p['id'] == project_id), None)

    def save_project(self, company_id, values, project_id=None):
        fields = tuple(values[key] for key in ('name','description','progress','start_date','end_date'))
        with self.connect() as db:
            if project_id is None:
                cursor = db.execute('''INSERT INTO design_projects
                    (company_id,name,description,progress,start_date,end_date)
                    VALUES (?,?,?,?,?,?)''', (company_id, *fields))
                return cursor.lastrowid
            db.execute('''UPDATE design_projects SET name=?,description=?,progress=?,
                start_date=?,end_date=?,updated_at=CURRENT_TIMESTAMP
                WHERE id=? AND company_id=?''', (*fields, project_id, company_id))
            return project_id

    def set_status(self, owner_id, status, project_id=None):
        with self.connect() as db:
            if project_id is None:
                db.execute('UPDATE designer_companies SET status=? WHERE owner_id=?', (status, owner_id))
            else:
                db.execute('''UPDATE design_projects SET status=?,updated_at=CURRENT_TIMESTAMP
                    WHERE id=? AND company_id=(SELECT id FROM designer_companies WHERE owner_id=?)''',
                    (status, project_id, owner_id))
