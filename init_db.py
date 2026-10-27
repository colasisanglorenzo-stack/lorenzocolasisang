import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
''')

# Clear existing student records
cursor.execute("DELETE FROM students")

# Sample student records
students = [
    ('2024-00156', 'Jade Warren Casas', 'BSIT', 2, 'A'),
    ('2024-00264', 'Renier Calambro', 'BSIT', 2, 'A'),
    ('2024-00125', 'Adrian Bunayos', 'BSIT', 3, 'B'),
    ('2024-00184', 'Lorenzo Colasisang', 'BSIT', 3, 'A'),
    ('2024-00347', 'Kate Ashley Distura', 'BSIT', 3, 'B'),
    ('2024-00087', 'Kc Jane Marie Ladoing', 'BSIT', 3, 'B'),
]

# Insert student records into the database
cursor.executemany('''
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

# Save changes and close the connection
conn.commit()
conn.close()

print("Database created successfully.")
