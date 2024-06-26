from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

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
    assert isinstance(student_id, str)


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

def test_get_student_non_existing():
    non_existing_id = str(uuid4())
    response = client.get(f"/student/{non_existing_id}")
    assert response.status_code == 404

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

def test_delete_student_non_existing():
    non_existing_id = str(uuid4())
    response = client.delete(f"/student/{non_existing_id}")
    assert response.status_code == 404

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