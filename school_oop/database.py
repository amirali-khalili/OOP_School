# database.py
import sqlite3


def get_connection():
    conn = sqlite3.connect("people.db")
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grade (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        score REAL NOT NULL,
        FOREIGN KEY(student_id) REFERENCES student(id),
        FOREIGN KEY(course_id) REFERENCES course(id),
        FOREIGN KEY(teacher_id) REFERENCES teacher(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_course (
    teacher_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (teacher_id, course_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS car (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id)
    );
    """)

    conn.commit()
    conn.close()


create_tables()

print("✅ Database and tables created successfully!")
