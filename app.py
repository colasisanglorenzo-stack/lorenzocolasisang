
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATABASE = "students.db"


# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create the students table automatically
def initialize_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Student Information API
@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00184",
        "name": "Lorenzo Colasisang",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# Greeting API
@app.route("/hello")
def hello():
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({
            "message": "Hello! Please enter your name."
        }), 400

    return jsonify({
        "message": f"Hello, {name}! Welcome to the Student API."
    })


# Course Information API
@app.route("/course")
def get_course():
    return jsonify({
        "course_code": "IT 303",
        "course_title": "Application Programming Interface",
        "instructor": "Course Instructor",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# Display all students saved in SQLite
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()

    try:
        students = conn.execute("""
            SELECT student_id, name, program, year, section
            FROM students
            ORDER BY student_id
        """).fetchall()

        return jsonify([dict(student) for student in students])

    finally:
        conn.close()


# Add a student to the database using POST
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Please send student data as JSON."
        }), 400

    student_id = str(data.get("student_id", "")).strip()
    name = str(data.get("name", "")).strip()
    program = str(data.get("program", "")).strip()
    section = str(data.get("section", "")).strip()

    try:
        year = int(data.get("year", 0))
    except (TypeError, ValueError):
        return jsonify({
            "error": "Year must be a number."
        }), 400

    if not all([student_id, name, program, section]) or year < 1:
        return jsonify({
            "error": (
                "Please provide student_id, name, program, "
                "year, and section."
            )
        }), 400

    conn = get_db_connection()

    try:
        conn.execute("""
            INSERT INTO students (
                student_id, name, program, year, section
            )
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, name, program, year, section))

        conn.commit()

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "That student ID already exists."
        }), 409

    finally:
        conn.close()

    return jsonify({
        "message": "Student added successfully.",
        "student": {
            "student_id": student_id,
            "name": name,
            "program": program,
            "year": year,
            "section": section
        }
    }), 201


# Additional API: Display students by program
@app.route("/students/program/<program>", methods=["GET"])
def get_students_by_program(program):
    conn = get_db_connection()

    try:
        students = conn.execute("""
            SELECT student_id, name, program, year, section
            FROM students
            WHERE program = ? COLLATE NOCASE
            ORDER BY student_id
        """, (program.strip(),)).fetchall()

        return jsonify([dict(student) for student in students])

    finally:
        conn.close()


# Additional API: Display students by year level
@app.route("/students/year/<int:year>", methods=["GET"])
def get_students_by_year(year):
    conn = get_db_connection()

    try:
        students = conn.execute("""
            SELECT student_id, name, program, year, section
            FROM students
            WHERE year = ?
            ORDER BY student_id
        """, (year,)).fetchall()

        return jsonify([dict(student) for student in students])

    finally:
        conn.close()


# Start the application
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
