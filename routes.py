from fastapi import APIRouter, HTTPException
from models import Student
from uuid import UUID, uuid4
from database import load_database  # Assurez-vous que cette fonction est correctement définie pour charger la base de données

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.post("/student/", response_model=UUID)
async def create_student(student: Student):
    load_database[student.id] = student.dict()
    return student.id

@router.get("/student/{student_id}", response_model=Student)
async def get_student(student_id: UUID):
    student = load_database.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**student)

@router.delete("/student/{student_id}")
async def delete_student(student_id: UUID):
    if student_id in load_database:
        del load_database[student_id]
        return {"message": "Student deleted"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")