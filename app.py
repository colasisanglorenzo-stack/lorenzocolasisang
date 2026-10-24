
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api")
def api():
    return "Welcome to my first API"


@app.route('/student')
def get_student():
    return jsonify({
         "student_id": "24-00184",
        "name": "Lorenzo Colasisang",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Course information API
@app.route('/course', methods=['GET'])
def get_course():
    return jsonify({
        "course_code": "CC101",
        "course_title": "Introduction to Computing",
        "instructor": "Instr. Rene Ardou",
        "semester": "1st Semester",
        "academic_year": "2026-2027"
    })


if __name__ == '__main__':
    app.run(debug=True)