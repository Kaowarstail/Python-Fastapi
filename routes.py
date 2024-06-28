from fastapi import APIRouter, HTTPException
from models import Student, Grade  # Importing Student and Grade models
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from uuid import UUID, uuid4  # Importing UUID for unique identifier operations
from database import load_database, save_database  # Importing database operations

router = APIRouter()  # Creating a new API router

# Endpoint to create a new student
@router.post("/student/", response_model=UUID)
async def create_student(student: Student):
    db = load_database()  # Load the database
    student_id = uuid4()  # Generate a unique ID for the new student
    student.id = student_id  # Assign the generated ID to the student
    db[student_id] = student.model_dump()  # Save the student in the database
    save_database(db)  # Save changes to the database
    return student_id  # Return the new student's ID

# Endpoint to retrieve a student by their ID
@router.get("/student/{student_id}", response_model=Student)
async def get_student(student_id: UUID):
    db = load_database()  # Load the database
    student = db.get(student_id)  # Attempt to get the student by ID
    if student is None:  # If the student does not exist
        raise HTTPException(status_code=404, detail="Student not found")  # Return an error
    return Student(**student)  # Return the found student

# Endpoint to delete a student by their ID
@router.delete("/student/{student_id}")
async def delete_student(student_id: UUID):
    db = load_database()  # Load the database
    if student_id in db:  # If the student exists
        del db[student_id]  # Delete the student from the database
        save_database(db)  # Save changes to the database
        return {"message": "Student deleted"}  # Return a success message
    else:
        raise HTTPException(status_code=404, detail="Student not found")  # Return an error if student not found

# Endpoint to retrieve a specific grade of a student
@router.get("/student/{student_id}/grades/{grade_id}", response_model=Grade)
async def get_student_grade(student_id: UUID, grade_id: UUID):
    db = load_database()  # Load the database
    student = db.get(student_id)  # Attempt to get the student by ID
    if student is None:  # If the student does not exist
        raise HTTPException(status_code=404, detail="Student not found")  # Return an error
    for grade in student['grades']:  # Iterate through the student's grades
        try:
            grade_uuid = UUID(grade['id'], version=4)  # Attempt to parse the grade's ID as a UUID
        except ValueError:
            continue  # Skip this grade if its ID is invalid
        if grade_uuid == grade_id:  # If the grade's ID matches the requested ID
            return Grade(**grade)  # Return the grade
    raise HTTPException(status_code=404, detail="Grade not found")  # Return an error if grade not found

# Endpoint to delete a specific grade of a student
@router.delete("/student/{student_id}/grades/{grade_id}")
async def delete_student_grade(student_id: UUID, grade_id: UUID):
    db = load_database()  # Load the database
    student = db.get(str(student_id))  # Attempt to get the student by ID
    if student is None:  # If the student does not exist
        raise HTTPException(status_code=404, detail="Student not found")  # Return an error
    grades = student['grades']  # Get the student's grades
    grade_index = next((index for (index, d) in enumerate(grades) if UUID(d["id"]) == grade_id), None)  # Find the index of the requested grade
    if grade_index is None:  # If the grade does not exist
        raise HTTPException(status_code=404, detail="Grade not found")  # Return an error
    del grades[grade_index]  # Delete the grade
    student['grades'] = grades  # Update the student's grades
    db[str(student_id)] = student  # Save the updated student in the database
    save_database(db)  # Save changes to the database
    return {"message": "Grade deleted"}  # Return a success message

# Endpoint to export data in different formats
@router.get("/export")
async def export_data(format: str = "csv"):
    db = load_database()  # Load the database
    if format == "json":  # If the requested format is JSON
        # Convert UUIDs to strings for JSON export
        json_db = {str(student_id): {**student_data, "id": str(student_id)} for student_id, student_data in db.items()}
        return JSONResponse(content=json_db)  # Return the database as a JSON response
    elif format == "csv":  # If the requested format is CSV
        csv_content = "id,first_name,last_name,email\n"  # CSV header
        for student_id, student_data in db.items():
            # Append each student's data to the CSV content
            csv_content += f"{student_id},{student_data['first_name']},{student_data['last_name']},{student_data['email']}\n"
        return PlainTextResponse(content=csv_content)  # Return the CSV content as plain text
    else:
        raise HTTPException(status_code=400, detail="Invalid format")  # Return an error if the format is invalid

# Endpoint to return a personalized greeting in HTML
@router.get("/{name}", response_class=HTMLResponse)
async def read_name(name: str):
    return f"<h1>Hello <span>{name}</span></h1>"  # Return a greeting with the provided name in HTML format