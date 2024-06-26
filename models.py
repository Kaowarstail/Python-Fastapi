from pydantic import BaseModel, EmailStr, Field, UUID4
from typing import List

class Grade(BaseModel):
    id: UUID4
    course: str
    score: int

class Student(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr
    grades: List[Grade]