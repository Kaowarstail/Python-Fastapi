import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import List, Optional
from uuid import uuid4, UUID

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

# Charger la base de données
def load_database():
    with open("database.json", "r") as db_file:
        data = json.load(db_file)
        # Charger les ID en tant que UUID directement
        for student in data["students"]:
            student["id"] = UUID(str(student["id"]))
            for grade in student["grades"]:
                # Assurez-vous que l'ID de grade est une chaîne bien formée avant de la convertir en UUID
                try:
                    grade["id"] = UUID(str(grade["id"]))
                except ValueError:
                    # Générer un nouvel UUID si l'ID de grade n'est pas valide
                    grade["id"] = uuid4()
        return {UUID(str(student["id"])): student for student in data["students"]}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)