from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_note(client):
    response = client.post("/notes", json={"name": "Test Note", "description": "This is a test"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Note"
    
def test_get_all_notes(client):
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_note_by_id(client):
    create_response = client.post("/notes", json={"name": "Note 1", "description": "Description 1"})
    note_id = create_response.json()["id"]
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Note 1"

def test_update_note(client):
    create_response = client.post("/notes", json={"name": "Old Name", "description": "Old Description"})
    note_id = create_response.json()["id"]
    response = client.put(f"/notes/{note_id}", json={"id": note_id, "name": "Updated Name", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_note(client):
    create_response = client.post("/notes", json={"name": "To Delete", "description": "Delete me"})
    note_id = create_response.json()["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert "has been deleted" in response.json()["message"]
    
def test_summarize_note_by_id(client):
    create_response = client.post("/notes", json={"name": "Summarize", "description": "This is a long text that needs to be summarized"})
    note_id = create_response.json()["id"]
    response = client.post(f"/notes/summarize/{note_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), str)
    
def test_get_analytics(client):
    response = client.get("/analytics")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    