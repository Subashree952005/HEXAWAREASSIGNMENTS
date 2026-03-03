from typing import Generic, List, TypeVar
from pydantic import BaseModel
from fastapi import Query

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(20, ge=1, le=100, description="Items per page"),
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    pages: int
    items: List[T]

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams):
        pages = (total + params.size - 1) // params.size
        return cls(total=total, page=params.page, size=params.size, pages=pages, items=items)