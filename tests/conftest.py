"""
Fixtures for setting up and tearing down the database and test client
for FastAPI endpoints using pytest.

Fixtures:
    - setup_database: Set up the MySQL engine once per test session, ensuring the database
      connection is ready for use across multiple tests.
    - db_session: Provide a scoped database session for each individual test function,
      managing transactions and ensuring isolation between tests.
    - client: Create a test client for interacting with the FastAPI app, allowing API 
      endpoints to be tested.
"""

import pytest
from fastapi.testclient import TestClient

from app import app
from connector.mysql_connector import MySQLConnector



@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Initialize the MySQL database engine at the start of the test session.

    This fixture runs automatically before any tests are executed.
    """
    MySQLConnector.create_engine()

@pytest.fixture(scope="function")
def db_session():
    """
    Provide a scoped database session for each test function.

    Ensure the database session is opened and closed properly with each test.
    """
    with MySQLConnector.session_scope() as session:
        yield session

@pytest.fixture(scope="function")
def client(db_session):
    """
    Provide a FastAPI test client for each test function.

    This allows interaction with the FastAPI application.
    It depends on the 'db_session' fixture to ensure database transactions are handled.
    """
    with TestClient(app) as test_client:
        yield test_client
