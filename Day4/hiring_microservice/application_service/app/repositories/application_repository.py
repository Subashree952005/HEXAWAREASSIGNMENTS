from sqlalchemy.orm import Session
from app.models.application import Application


class ApplicationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_application(self, data: dict) -> Application:
        application = Application(**data)
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_applications_by_user(self, user_id: int):
        return self.db.query(Application).filter(Application.user_id == user_id).all()

    def get_application_by_id(self, app_id: int):
        return self.db.query(Application).filter(Application.id == app_id).first()