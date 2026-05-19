from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

students_data = []

csv_path = "students.csv"

if os.path.exists(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            students_data.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })

@app.get("/")
async def home():
    return {"message": "Student API running"}

@app.get("/api")
async def get_students(
    class_: list[str] | None = Query(default=None, alias="class")
):

    if class_:
        filtered = [
            student for student in students_data
            if student["class"] in class_
        ]
        return {"students": filtered}

    return {"students": students_data}