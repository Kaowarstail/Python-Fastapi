from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

# Modèles Pydantic
class Grade(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    course: str
    score: int = Field(..., ge=0, le=100)

class Student(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade] = []

# Base de données fictive
students_db = {}

@app.get("/")
async def read_root(name: Optional[str] = None):
    return {"message": f"Hello {name}"}

@app.post("/student/", response_model=UUID4)
async def create_student(student: Student):
    students_db[student.id] = student
    return student.id

@app.get("/student/{student_id}", response_model=Student)
async def get_student(student_id: UUID4):
    student = students_db.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/student/{student_id}")
async def delete_student(student_id: UUID4):
    if student_id in students_db:
        del students_db[student_id]
        return {"message": "Student deleted"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# Ajoutez d'autres endpoints ici selon les spécifications

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)