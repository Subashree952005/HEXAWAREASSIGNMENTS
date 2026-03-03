from fastapi import FastAPI

from app.middleware.cors import add_cors_middleware

# Routers (we will create these soon)
from app.controllers.student_controller import router as student_router
from app.controllers.course_controller import router as course_router
from app.controllers.enrollment_controller import router as enrollment_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="LMS Course Enrollment API",
        version="1.0.0",
        description="Backend system for managing students, courses, and enrollments",
    )

    # Middleware
    add_cors_middleware(app)

    # Routers
    app.include_router(student_router, prefix="/students", tags=["Students"])
    app.include_router(course_router, prefix="/courses", tags=["Courses"])
    app.include_router(enrollment_router, prefix="/enrollments", tags=["Enrollments"])

    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "LMS API is running"}
