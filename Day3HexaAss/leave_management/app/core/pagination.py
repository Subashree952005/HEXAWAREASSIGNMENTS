from fastapi import Query
from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        size: int = Query(default=10, ge=1, le=100)
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size
        self.limit = size

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]