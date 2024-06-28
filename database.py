import json  # Importing the json module for loading and saving JSON data
from uuid import UUID  # Importing UUID for handling UUID objects
from models import Student  # Importing the Student model from models.py

# Functions to load and save the database

def load_database():
    with open("database.json", "r") as db_file:  # Opening the database file in read mode
        data = json.load(db_file)  # Loading the JSON data from the file
        # Converting the IDs to UUID objects
        return {UUID(student["id"]): student for student in data["students"]}  # Returning a dictionary with UUID keys

def save_database(db):
    with open("database.json", "w") as db_file:  # Opening the database file in write mode
        # Preparing the data for saving
        data = {"students": [student for student in db.values()]}  # Creating a list of students from the database dictionary
        json.dump(data, db_file, indent=4, default=str)  # Saving the JSON data to the file with indentation

