import pytest
from fastapi.testclient import TestClient
from unittest import mock
from uuid import uuid4, UUID
from main import app  # Ensure this import matches the structure of your project

client = TestClient(app)

@pytest.fixture
def mock_post(monkeypatch):
    def mock_function(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
        return MockResponse({"id": str(uuid4())}, 200)
    monkeypatch.setattr("requests.post", mock_function)

@pytest.fixture
def mock_get(monkeypatch):
    def mock_function(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
        if "grades" in args[0]:
            return MockResponse({"id": "12d6cb45-210d-4609-b90d-53ff41db6f0a", "course": "Math", "score": 95}, 200)
        elif "export" in args[0]:
            if "format=json" in args[0]:
                return MockResponse([{"id": "123e4567-e89b-12d3-a456-426614174000", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}], 200)
            elif "format=csv" in args[0]:
                return MockResponse("id,first_name,last_name,email\n123e4567-e89b-12d3-a456-426614174000,John,Doe,john.doe@example.com", 200, content_type="text/csv")
            else:
                return MockResponse({"detail": "Invalid format"}, 400)
        else:
            return MockResponse({"id": str(uuid4()), "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "grades": []}, 200)
    monkeypatch.setattr("requests.get", mock_function)

@pytest.fixture
def mock_delete(monkeypatch):
    def mock_function(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
        return MockResponse({"message": "Student deleted"}, 200)
    monkeypatch.setattr("requests.delete", mock_function)


def test_create_student():
    student_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "grades": []
    }
    response = client.post("/student/", json=student_data)
    assert response.status_code == 200
    student_id = response.json()
    assert UUID(student_id, version=4)

def test_get_student_existing():
    student_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "grades": []
    }
    create_response = client.post("/student/", json=student_data)
    student_id = create_response.json()
    
    response = client.get(f"/student/{student_id}")
    assert response.status_code == 200
    retrieved_student = response.json()
    assert retrieved_student["id"] == student_id
    assert retrieved_student["first_name"] == "Jane"
    assert retrieved_student["last_name"] == "Doe"

def test_delete_student_existing():
    student_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "grades": []
    }
    create_response = client.post("/student/", json=student_data)
    student_id = create_response.json()
    
    response = client.delete(f"/student/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted"}

def test_export_data_csv():
    response = client.get("/export?format=csv")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert content.startswith("id,first_name,last_name,email\n")
    assert len(content.split("\n")) > 1

def test_export_data_json():
    response = client.get("/export?format=json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_export_data_invalid_format():
    response = client.get("/export?format=xml")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid format"}

def test_get_student_grade_existing():
    # Assuming a student with grades already exists, fetch a specific grade
    student_id = "123e4567-e89b-12d3-a456-426614174000" 
    grade_id = "123e4567-e89b-12d3-a456-426614174009"
    response = client.get(f"/student/{student_id}/grades/{grade_id}")
    assert response.status_code == 200
    grade = response.json()
    assert grade["id"] == grade_id
    assert "course" in grade
    assert "score" in grade

def test_delete_student_grade_existing():
    # Assuming a student with grades already exists, delete a specific grade
    student_id = "123e4567-e89b-12d3-a456-426614174000"
    grade_id = "123e4567-e89b-12d3-a456-426614174009"
    response = client.delete(f"/student/{student_id}/grades/{grade_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Grade deleted"}