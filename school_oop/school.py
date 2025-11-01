from abc import ABC, abstractmethod

from database import *


class IDatabase(ABC):
    @abstractmethod
    def get_connection(self):
        pass


class SQLiteDB(IDatabase):
    def __init__(self, path):
        self.path = path

    def get_connection(self):
        return sqlite3.connect(self.path)


class Person(ABC):
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @abstractmethod
    def introduce(self):
        pass


# ---------------- Course ----------------
class Course:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __repr__(self):
        return f"Course({self.name})"


class CourseRepository:
    def __init__(self, db: IDatabase):
        self.db = db

    def save(self, course: Course):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO course (name) VALUES (?)", (course.name,))
        conn.commit()
        conn.close()


# ---------------- Student ----------------
class Student(Person):
    def __init__(self, name, age):
        super().__init__(name, age)

    def introduce(self):
        print(f"Name: {self.name}, Age: {self.age}")

    def __repr__(self):
        return f"Student({self.name}, {self.age})"


class StudentRepository:
    def __init__(self, db: IDatabase):
        self.db = db

    def save(self, student: Student):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (name, age) VALUES (?, ?)", (student.name, student.age)
        )
        conn.commit()
        conn.close()


class StudentService:
    def __init__(self, db: IDatabase):
        self.db = db

    def average_score(self, student_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT AVG(score) FROM grade WHERE student_id = ?", (student_id,)
        )
        avg = cursor.fetchone()[0]
        conn.close()
        return avg or 0


# ---------------- Teacher ----------------
class Teacher(Person):
    def introduce(self):
        print(f"Name: {self.name}, Age: {self.age}")

    def __repr__(self):
        return f"Teacher({self.name}, {self.age})"


class TeacherRepository:
    def __init__(self, db: IDatabase):
        self.db = db

    def save(self, teacher: Teacher):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO teacher (name, age) VALUES (?, ?)", (teacher.name, teacher.age)
        )
        conn.commit()
        conn.close()


class TeacherService:
    def __init__(self, db: IDatabase):
        self.db = db

    def assign_course(self, teacher_id: int, course_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO teacher_course (teacher_id, course_id) VALUES (?, ?)",
            (teacher_id, course_id),
        )
        conn.commit()
        conn.close()

    def show_courses(self, teacher_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.name
            FROM course c
            JOIN teacher_course tc ON c.id = tc.course_id
            WHERE tc.teacher_id = ?
            """,
            (teacher_id,),
        )
        courses = cursor.fetchall()
        conn.close()
        return [c[0] for c in courses]

    def give_grade(
        self, teacher_id: int, student_id: int, course_id: int, score: float
    ):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grade (student_id, course_id, teacher_id, score) VALUES (?, ?, ?, ?)",
            (student_id, course_id, teacher_id, score),
        )
        conn.commit()
        conn.close()


# ---------------- Car ----------------
class Car:
    def __init__(self, name, teacher_id):
        self.name = name
        self.teacher_id = teacher_id


class CarRepository:
    def __init__(self, db: IDatabase):
        self.db = db

    def save(self, car: Car):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO car (name, teacher_id) VALUES (?, ?)",
            (car.name, car.teacher_id),
        )
        conn.commit()
        conn.close()
