from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.asset_service import AssetService
from app.services.assignment_service import AssignmentService
from app.services.request_service import RequestService
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn
from app.schemas.request_schema import AssetRequestApprove, AssetRequestReject
from app.models.asset import AssetStatus, AssetType
from app.models.asset_request import RequestStatus
from app.core.pagination import PaginationParams


class ITAdminController:
    def __init__(self, db: AsyncSession):
        self.asset_svc = AssetService(db)
        self.assignment_svc = AssignmentService(db)
        self.request_svc = RequestService(db)

    # ── Assets ─────────────────────────────────────────────
    async def create_asset(self, data: AssetCreate):
        return await self.asset_svc.create_asset(data)

    async def list_assets(
        self,
        params: PaginationParams,
        status: Optional[AssetStatus] = None,
        asset_type: Optional[AssetType] = None,
        department_id: Optional[int] = None,
        search: Optional[str] = None,
    ):
        return await self.asset_svc.list_assets(params, status, asset_type, department_id, search)

    async def get_asset(self, asset_id: int):
        return await self.asset_svc.get_asset(asset_id)

    async def update_asset(self, asset_id: int, data: AssetUpdate):
        return await self.asset_svc.update_asset(asset_id, data)

    async def delete_asset(self, asset_id: int):
        return await self.asset_svc.delete_asset(asset_id)

    # ── Assignments ────────────────────────────────────────
    async def assign_asset(self, data: AssignmentCreate, assigned_by: int):
        return await self.assignment_svc.assign_asset(data, assigned_by)

    async def list_assignments(self, params: PaginationParams):
        return await self.assignment_svc.list_assignments(params)

    async def return_asset(self, assignment_id: int, data: AssignmentReturn):
        return await self.assignment_svc.return_asset(assignment_id, data)

    # ── Requests ───────────────────────────────────────────
    async def list_requests(self, params: PaginationParams, status: Optional[RequestStatus] = None):
        return await self.request_svc.list_requests(params, status)

    async def approve_request(self, req_id: int, data: AssetRequestApprove, approver_id: int):
        return await self.request_svc.approve_request(req_id, data, approver_id)

    async def reject_request(self, req_id: int, data: AssetRequestReject, approver_id: int):
        return await self.request_svc.reject_request(req_id, data, approver_id)