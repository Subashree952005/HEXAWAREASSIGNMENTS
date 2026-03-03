from app.repositories import enrollment_repository, student_repository, course_repository

def enroll_student(student_id: int, course_id: int):
    if not student_repository.get_student(student_id):
        raise ValueError("Student not found")

    if not course_repository.get_course(course_id):
        raise ValueError("Course not found")

    existing = enrollment_repository.find_enrollment(student_id, course_id)
    if existing:
        raise ValueError("Already enrolled")

    return enrollment_repository.create_enrollment(student_id, course_id)

def get_all_enrollments():
    return enrollment_repository.get_all_enrollments()

def get_enrollments_by_student(student_id: int):
    return enrollment_repository.get_enrollments_by_student(student_id)

def get_enrollments_by_course(course_id: int):
    return enrollment_repository.get_enrollments_by_course(course_id)
