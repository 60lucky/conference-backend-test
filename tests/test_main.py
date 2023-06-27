import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from backend.main import app
from backend.models import Base
from backend.schemas import InstitutionCreate, UserCreate


@pytest.fixture(scope="module")
def test_db():
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    session = Session(bind=connection)
    yield session
    session.close()
    connection.close()
    engine.dispose()


@pytest.fixture(scope="module")
def test_client():
    # Create a test client using the FastAPI app
    client = TestClient(app)
    yield client


def test_create_institution(test_db, test_client):
    # Create a test institution
    institution_data = {
        "institutionName": "Example Institution",
        "institutionAddress": "123 Main Street",
        "emailID": "example@example.com",
        "contactNum": 1234567890,
        "membership": "Choice1",
    }
    response = test_client.post("/institutions", json=institution_data)
    assert response.status_code == 200
    created_institution = response.json()
    assert created_institution["institutionName"] == institution_data["institutionName"]
    assert created_institution["institutionAddress"] == institution_data["institutionAddress"]
    assert created_institution["emailID"] == institution_data["emailID"]
    assert created_institution["contactNum"] == institution_data["contactNum"]
    assert created_institution["membership"] == institution_data["membership"]


def test_create_admin(test_db, test_client):
    # Create a test admin
    admin_data = {
        "name": "admin",
        "password": "password",
        "email": "admin@example.com",
    }
    response = test_client.post("/admins", json=admin_data)
    assert response.status_code == 200
    created_admin = response.json()
    assert created_admin["name"] == admin_data["name"]


def test_assign_admin_to_institution(test_db, test_client):
    # Create a test institution
    institution_data = {
        "institutionName": "Example Institution",
        "institutionAddress": "123 Main Street",
        "emailID": "example@example.com",
        "contactNum": 1234567890,
        "membership": "Choice1",
    }
    response = test_client.post("/institutions", json=institution_data)
    assert response.status_code == 200
    created_institution = response.json()

    # Create a test admin
    admin_data = {
        "name": "admin",
        "password": "password",
        "email": "admin@example.com",
    }
    response = test_client.post("/admins", json=admin_data)
    assert response.status_code == 200
    created_admin = response.json()

    # Assign the admin to the institution
    response = test_client.put(
        f"/admins/{created_admin['userID']}/institution?institution_id={created_institution['institutionID']}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Admin assigned to the institution successfully"}
