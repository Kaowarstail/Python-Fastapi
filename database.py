import json
from uuid import UUID
from models import Student

def load_database():
    with open("database.json", "r") as db_file:
        data = json.load(db_file)
        # Conversion des ID en UUID
        return {UUID(student["id"]): student for student in data["students"]}
    
def save_database(db):
    with open("database.json", "w") as db_file:
        # Préparation des données pour la sauvegarde
        data = {"students": [student for student in db.values()]}
        json.dump(data, db_file, indent=4, default=str)