from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import List, Optional
from uuid import uuid4, UUID
import json

app = FastAPI()

# Modèles Pydantic
class Grade(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    course: str
    score: int = Field(..., ge=0, le=20)

class Student(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade] = []

# Charger la base de données
def load_database():
    with open("database.json", "r") as db_file:
        data = json.load(db_file)
        # Convertir les ID en UUID sans les convertir en chaînes
        for student in data["students"]:
            # Assurez-vous que l'ID est un entier long pour UUID
            student["id"] = UUID(int=student["id"])
            for grade in student["grades"]:
                # De même pour les ID des notes
                grade["id"] = UUID(int=grade["id"])
        return {student["id"]: student for student in data["students"]}

students_db = load_database()

@app.get("/")
async def read_root(name: Optional[str] = None):
    return {"message": f"Hello {name if name else 'world'}"}

@app.post("/student/", response_model=UUID4)
async def create_student(student: Student):
    students_db[student.id] = student.dict()
    return student.id

@app.get("/student/{student_id}", response_model=Student)
async def get_student(student_id: UUID4):
    student = students_db.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**student)

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