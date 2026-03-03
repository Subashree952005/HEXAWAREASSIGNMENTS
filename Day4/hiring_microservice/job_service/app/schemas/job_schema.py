from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    company: str


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    company: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    company: str

    model_config = ConfigDict(from_attributes=True)