from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my first API!"

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00184",
        "name": "Lorenzo Colasisang",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })

@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "CC101",
        "course_title": "Introduction to Computing",
        "instructor": "Instr. Rene Ardou ",
        "semester": "1st Semester",
        "academic_year": "2026-2027"
    })

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })

@app.route('/greet')
def personalized_greeting():
    name = request.args.get('name', 'Lorenzo')
    section = request.args.get('section', 'BSIT3A - Hamilton')
    return jsonify({
        "message": f"Hello {name} from {section}!"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)