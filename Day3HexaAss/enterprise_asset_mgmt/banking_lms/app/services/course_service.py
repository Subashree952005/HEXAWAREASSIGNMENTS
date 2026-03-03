from app.repositories import course_repository

def create_course(title: str, duration: int):
    return course_repository.create_course(title, duration)

def get_course(course_id: int):
    course = course_repository.get_course(course_id)
    if not course:
        raise ValueError("Course not found")
    return course

def list_courses():
    return course_repository.list_courses()
