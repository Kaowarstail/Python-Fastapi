import pytest
import json
from fastapi.testclient import TestClient
from starlette.responses import Response  
from uuid import uuid4, UUID
from main import app

client = TestClient(app)

# Chargement des données de test à partir de database.json
with open("database.json") as f:
    database = json.load(f)

def mock_post(monkeypatch):
    def mock_function(*args, **kwargs):
        # Génère un nouvel ID d'étudiant et simule l'ajout à la base de données
        new_id = str(UUID(int=UUID("123e4567-e89b-12d3-a456-426614174000").int + len(database["students"])))
        # Adjusted to use Response instead of MockResponse
        return Response(content=json.dumps({"id": new_id}), status_code=200)
    monkeypatch.setattr("requests.post", mock_function)

# Adjust the rest of the mock functions similarly...
def mock_get(monkeypatch):

    def mock_function(*args, **kwargs):
        url = args[0]
        student_id = url.split("/student/")[1].split("/")[0]
        grade_id = url.split("/grades/")[1] if "/grades/" in url else None

        if "grades" in url and grade_id:
            for student in database["students"]:
                if student["id"] == student_id:
                    for grade in student["grades"]:
                        if grade["id"] == grade_id:
                            return Response(content=json.dumps(grade), status_code=200)
        elif "export" in url:
            if "format=json" in url:
                return Response(content=json.dumps(database["students"]), status_code=200)
            elif "format=csv" in url:
                csv_data = "id,first_name,last_name,email\n" + "\n".join(
                    f'{student["id"]},{student["first_name"]},{student["last_name"]},{student["email"]}' for student in database["students"])
                return Response(content=csv_data, status_code=200, media_type="text/csv")
        else:
            for student in database["students"]:
                if student["id"] == student_id:
                    return Response(content=json.dumps(student), status_code=200)
        return Response(content=json.dumps({"detail": "Not found"}), status_code=404)
    monkeypatch.setattr("requests.get", mock_function)

def mock_delete(monkeypatch):
    def mock_function(*args, **kwargs):
        return Response(content=json.dumps({"message": "Deleted successfully"}), status_code=200)
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
    student_id = "54e37f3c-ca5c-4876-bbf4-482a88190c83" 
    grade_id = "edf9f1ae-0220-4a91-b420-fb867b6b7fda"
    response = client.get(f"/student/{student_id}/grades/{grade_id}")
    assert response.status_code == 200
    grade = response.json()
    assert grade["id"] == grade_id
    assert "course" in grade
    assert "score" in grade
