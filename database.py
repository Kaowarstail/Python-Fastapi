import json
from uuid import UUID
from models import Student

def load_database():
    with open("database.json", "r") as db_file:
        data = json.load(db_file)
        # Conversion des ID en UUID
        return {UUID(student["id"]): student for student in data["students"]}