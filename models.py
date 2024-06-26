from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import UUID, uuid4

class Grade(BaseModel):
    id: UUID4
    course: str
    score: int

class Student(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    email: str
    grades: Optional[List[int]] = None