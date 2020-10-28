from pathlib import Path
import os
import pytest
from project.app import app, init_db

TEST_DB = "test.db"

@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    app.config["DATABASE"] = BASE_DIR.joinpath(TEST_DB)

    init_db() # Set up db
    yield app.test_client() # Run tests here
    init_db() # Teardown

def login(client, username, password):
    """Login Helper Function"""
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects = True
    )

def logout(client):
    """Logout helper function"""
    return client.get("/logout", follow_redirects=True)

def test_index(client):
    response = client.get("/", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"Hello, World!"

def test_database(client):
    """Initial test to ensure database exists"""
    init_db()
    tester = Path("test.db").is_file()
    assert tester

def test_empty_db(client):
    """Ensure db is blank"""
    rv = client.get("/")
    assert b"No entries yet. Add some!" in rv.data

def test_login_logout(client):
    """Test login and logout using helper functinos."""
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"])
    assert b"You were logged in" in rv.data

    rv = logout(client)
    assert b"You were logged out" in rv.data

    rv = login(client, app.config["USERNAME"] + "lol", app.config["PASSWORD"])
    assert b"Invalid username" in rv.data

    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "lol")
    assert b"Invalid password" in rv.data

def test_messages(client):
    """Ensure user can post messages"""
    login(client, app.config["USERNAME"], app.config["PASSWORD"])
    rv = client.post(
        "/add",
        data=dict(title="<Hello>", text="<strong>HTML</strong> allowed here"),
        follow_redirects=True
    )
    assert b"No entries here so far" not in rv.data
    assert b"&lt;Hello&gt;" in rv.data
    assert b"<strong>HTML</strong> allowed here" in rv.data