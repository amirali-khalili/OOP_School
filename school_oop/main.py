from database import *
from school import *

# Database
db = SQLiteDB("people.db")

# Repositories
student_repo = StudentRepository(db)
teacher_repo = TeacherRepository(db)
course_repo = CourseRepository(db)
car_repo = CarRepository(db)

# Services
student_service = StudentService(db)
teacher_service = TeacherService(db)


# Helper functions
def list_students():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM student")
    students = cursor.fetchall()
    conn.close()
    if not students:
        print("No students yet.")
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}, Age: {s[2]}")
    return students


def list_teachers():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM teacher")
    teachers = cursor.fetchall()
    conn.close()
    if not teachers:
        print("No teachers yet.")
    for t in teachers:
        print(f"ID: {t[0]}, Name: {t[1]}, Age: {t[2]}")
    return teachers


def list_courses():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM course")
    courses = cursor.fetchall()
    conn.close()
    if not courses:
        print("No courses yet.")
    for c in courses:
        print(f"ID: {c[0]}, Name: {c[1]}")
    return courses


def list_cars():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, c.name, t.name
        FROM car c
        LEFT JOIN teacher t ON c.teacher_id = t.id
    """)
    cars = cursor.fetchall()
    conn.close()
    if not cars:
        print("No cars yet.")
    for c in cars:
        print(f"ID: {c[0]}, Car: {c[1]}, Teacher: {c[2]}")
    return cars


while True:
    print("\n1. Add Student")
    print("2. Add Teacher")
    print("3. Add Course")
    print("4. Assign Course to Teacher")
    print("5. Give Grade")
    print("6. Show Student Average")
    print("7. Show Teacher Courses")
    print("8. List Teachers")
    print("9. List Students")
    print("10. List Courses")
    print("11. Add Car")
    print("12. List Cars")
    print("0. Exit")

    choice = input("Select: ")

    if choice == "1":
        name = input("Student name: ")
        age = int(input("Student age: "))
        student = Student(name, age)
        student_repo.save(student)
        print(f"Student {name} added ")

    elif choice == "2":
        name = input("Teacher name: ")
        age = int(input("Teacher age: "))
        teacher = Teacher(name, age)
        teacher_repo.save(teacher)
        print(f"Teacher {name} added ")

    elif choice == "3":
        name = input("Course name: ")
        course = Course(name)
        course_repo.save(course)
        print(f"{name} added ")

    elif choice == "4":
        teachers = list_teachers()
        tid = int(input("Select Teacher ID: "))
        courses = list_courses()
        cid = int(input("Select Course ID: "))
        teacher_service.assign_course(tid, cid)
        print(f"Course ID {cid} assigned to Teacher ID {tid}")

    elif choice == "5":
        students = list_students()
        sid = int(input("Select Student ID: "))
        teachers = list_teachers()
        tid = int(input("Select Teacher ID: "))
        courses = list_courses()
        cid = int(input("Select Course ID: "))
        score = float(input("Score: "))
        teacher_service.give_grade(tid, sid, cid, score)
        print(
            f"Student ID {sid} got score {score} in Course ID {cid} from Teacher ID {tid}"
        )

    elif choice == "6":
        students = list_students()
        sid = int(input("Select Student ID: "))
        avg = student_service.average_score(sid)
        print(f"Student ID {sid} average score: {avg}")

    elif choice == "7":
        teachers = list_teachers()
        tid = int(input("Select Teacher ID: "))
        courses = teacher_service.show_courses(tid)
        print(f"Teacher ID {tid} teaches: {courses}")

    elif choice == "8":
        list_teachers()

    elif choice == "9":
        list_students()

    elif choice == "10":
        list_courses()

    elif choice == "11":
        name = input("Car name: ")
        teachers = list_teachers()
        tid = int(input("Select Teacher ID: "))
        car = Car(name, tid)
        car_repo.save(car)
        print(f"Car {name} added for Teacher ID {tid} ")

    elif choice == "12":
        list_cars()

    elif choice == "0":
        break

    else:
        print("Invalid choice!")
