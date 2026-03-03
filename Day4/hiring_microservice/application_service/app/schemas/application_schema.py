from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)