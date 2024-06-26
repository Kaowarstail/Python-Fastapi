from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is initialized in a file named main.py
from models import Student
from uuid import uuid4

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_student():
    student_data = {"id": str(uuid4()), "name": "John Doe", "age": 20}
    response = client.post("/student/", json=student_data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)  # Assuming the response is the UUID of the created student

def test_get_student_existing():
    # First, create a student to ensure it exists
    student_data = {"id": str(uuid4()), "name": "Jane Doe", "age": 21}
    create_response = client.post("/student/", json=student_data)
    student_id = create_response.json()["id"]
    
    # Now, retrieve the created student
    response = client.get(f"/student/{student_id}")
    assert response.status_code == 200
    assert response.json()["id"] == student_id

def test_get_student_non_existing():
    non_existing_id = str(uuid4())
    response = client.get(f"/student/{non_existing_id}")
    assert response.status_code == 404

def test_delete_student_existing():
    # First, create a student to ensure it exists
    student_data = {"id": str(uuid4()), "name": "John Smith", "age": 22}
    create_response = client.post("/student/", json=student_data)
    student_id = create_response.json()["id"]
    
    # Now, delete the created student
    response = client.delete(f"/student/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Student deleted"}

def test_delete_student_non_existing():
    non_existing_id = str(uuid4())
    response = client.delete(f"/student/{non_existing_id}")
    assert response.status_code == 404