from app.core import db
from app.models.student_model import Student

def create_student(name: str, email: str):
    student = Student(db.student_id_counter, name, email)
    db.students[db.student_id_counter] = student
    db.student_id_counter += 1
    return student

def get_student(student_id: int):
    return db.students.get(student_id)
