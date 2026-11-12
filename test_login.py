
'''
What this code does?
- Test the User Account Entity's login authentication.
- Create temporary test accounts without affecting the real database.
- Test one successful login and three unsuccessful login scenarios.
'''

import sqlite3

import pytest
from werkzeug.security import generate_password_hash

from Entities.userAccount import UserAccount


# Prepare test accounts in a temporary database
@pytest.fixture
def login_accounts(tmp_path):

    test_db = tmp_path / "testUserAccount.db"

    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    # Create the account table required for login
    cursor.execute("""
        CREATE TABLE user_accounts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            password_hash TEXT,
            role TEXT,
            status TEXT,
            profile_id INTEGER
        )
    """)

    password_hash = generate_password_hash("CorrectPass123!")

    # Create an active test account
    cursor.execute("""
        INSERT INTO user_accounts
        (name, email, password_hash, role, status, profile_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Active Tester",
        "active@test.com",
        password_hash,
        "customer",
        "active",
        None
    ))

    # Create a suspended test account
    cursor.execute("""
        INSERT INTO user_accounts
        (name, email, password_hash, role, status, profile_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Suspended Tester",
        "suspended@test.com",
        password_hash,
        "customer",
        "suspended",
        None
    ))

    connection.commit()
    connection.close()

    # Point the Entity to the temporary database
    account = UserAccount()
    account.db_path = test_db

    return account


# Positive test: correct login credentials
def test_login_with_correct_credentials(login_accounts):

    result = login_accounts.authenticate_login({
        "email": "active@test.com",
        "password": "CorrectPass123!",
        "role": "customer"
    })

    assert result["data"]["success"] is True
    assert result["status_code"] == 200


# Negative test: incorrect password
def test_login_with_wrong_password(login_accounts):

    result = login_accounts.authenticate_login({
        "email": "active@test.com",
        "password": "WrongPass123!",
        "role": "customer"
    })

    assert result["data"]["success"] is False
    assert result["status_code"] == 401


# Negative test: unregistered email
def test_login_with_unknown_email(login_accounts):

    result = login_accounts.authenticate_login({
        "email": "unknown@test.com",
        "password": "CorrectPass123!",
        "role": "customer"
    })

    assert result["data"]["success"] is False
    assert result["status_code"] == 401


# Negative test: suspended account
def test_login_with_suspended_account(login_accounts):

    result = login_accounts.authenticate_login({
        "email": "suspended@test.com",
        "password": "CorrectPass123!",
        "role": "customer"
    })

    assert result["data"]["success"] is False
    assert result["status_code"] == 403
