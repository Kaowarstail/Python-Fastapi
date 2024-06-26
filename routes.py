from fastapi import APIRouter, HTTPException
from models import Student
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from uuid import UUID, uuid4
from database import load_database, save_database

router = APIRouter()

@router.post("/student/", response_model=UUID)
async def create_student(student: Student):
    db = load_database()
    student_id = uuid4()
    student.id = student_id
    db[student_id] = student.dict()
    save_database(db)
    return student_id

@router.get("/student/{student_id}", response_model=Student)
async def get_student(student_id: UUID):
    db = load_database()
    student = db.get(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**student)

@router.delete("/student/{student_id}")
async def delete_student(student_id: UUID):
    db = load_database()
    if student_id in db:
        del db[student_id]
        save_database(db)
        return {"message": "Student deleted"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
@router.get("/export")
async def export_data(format: str = "csv"):
    db = load_database()
    if format == "json":
        return JSONResponse(content=db)
    elif format == "csv":
        csv_content = "id,first_name,last_name,email\n"
        for student_id, student_data in db.items():
            csv_content += f"{student_id},{student_data['first_name']},{student_data['last_name']},{student_data['email']}\n"
        return PlainTextResponse(content=csv_content)
    else:
        raise HTTPException(status_code=400, detail="Invalid format")
    
@router.get("/{name}", response_class=HTMLResponse)
async def read_name(name: str):
    return f"<h1>Hello <span>{name}</span></h1>"