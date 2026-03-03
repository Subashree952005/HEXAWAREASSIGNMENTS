from app.core import db
from app.models.course_model import Course

def create_course(title: str, duration: int):
    course = Course(db.course_id_counter, title, duration)
    db.courses[db.course_id_counter] = course
    db.course_id_counter += 1
    return course

def get_course(course_id: int):
    return db.courses.get(course_id)

def list_courses():
    return list(db.courses.values())
