from app.repositories import student_repository

def register_student(name: str, email: str):
    return student_repository.create_student(name, email)

def get_student(student_id: int):
    student = student_repository.get_student(student_id)
    if not student:
        raise ValueError("Student not found")
    return student
