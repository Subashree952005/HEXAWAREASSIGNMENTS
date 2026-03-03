from sqlalchemy.ext.asyncio import AsyncSession

from app.services.assignment_service import AssignmentService
from app.services.request_service import RequestService
from app.schemas.request_schema import AssetRequestCreate
from app.core.pagination import PaginationParams


class EmployeeController:
    def __init__(self, db: AsyncSession):
        self.assignment_svc = AssignmentService(db)
        self.request_svc = RequestService(db)

    async def get_my_assets(self, user_id: int):
        return await self.assignment_svc.get_user_assignments(user_id)

    async def create_request(self, data: AssetRequestCreate, employee_id: int):
        return await self.request_svc.create_request(data, employee_id)

    async def get_my_requests(self, employee_id: int, params: PaginationParams):
        return await self.request_svc.get_my_requests(employee_id, params)