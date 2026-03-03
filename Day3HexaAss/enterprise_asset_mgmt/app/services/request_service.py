from typing import Optional
from datetime import date
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.request_repo import RequestRepo
from app.repositories.asset_repo import AssetRepo
from app.repositories.assignment_repo import AssignmentRepo
from app.schemas.request_schema import AssetRequestCreate, AssetRequestApprove, AssetRequestReject
from app.schemas.assignment_schema import AssignmentCreate
from app.models.asset_request import RequestStatus
from app.models.asset import AssetStatus
from app.core.pagination import PaginationParams, PaginatedResponse


class RequestService:
    def __init__(self, db: AsyncSession):
        self.repo = RequestRepo(db)
        self.asset_repo = AssetRepo(db)
        self.assignment_repo = AssignmentRepo(db)

    async def create_request(self, data: AssetRequestCreate, employee_id: int):
        return await self.repo.create(data, employee_id)

    async def get_my_requests(self, employee_id: int, params: PaginationParams):
        items, total = await self.repo.get_all(
            offset=params.offset, limit=params.size, employee_id=employee_id
        )
        return PaginatedResponse.create(items, total, params)

    async def list_requests(self, params: PaginationParams, status: Optional[RequestStatus] = None):
        items, total = await self.repo.get_all(offset=params.offset, limit=params.size, status=status)
        return PaginatedResponse.create(items, total, params)

    async def approve_request(self, req_id: int, data: AssetRequestApprove, approver_id: int):
        req = await self.repo.get_by_id(req_id)
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        if req.status != RequestStatus.PENDING:
            raise HTTPException(status_code=400, detail=f"Request is already {req.status}")

        asset = await self.asset_repo.get_by_id(data.asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        if asset.status != AssetStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail="Selected asset is not available")
        if asset.asset_type != req.asset_type:
            raise HTTPException(
                status_code=400,
                detail=f"Asset type mismatch. Request needs {req.asset_type}, got {asset.asset_type}"
            )

        # Approve the request
        await self.repo.approve(req, approver_id)

        # Create assignment
        assignment_data = AssignmentCreate(
            asset_id=data.asset_id,
            user_id=req.employee_id,
            assigned_date=date.today(),
        )
        assignment = await self.assignment_repo.create(assignment_data, approver_id)
        await self.asset_repo.update_status(asset, AssetStatus.ASSIGNED)

        return {"request": req, "assignment": assignment}

    async def reject_request(self, req_id: int, data: AssetRequestReject, approver_id: int):
        req = await self.repo.get_by_id(req_id)
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        if req.status != RequestStatus.PENDING:
            raise HTTPException(status_code=400, detail=f"Request is already {req.status}")
        return await self.repo.reject(req, approver_id, data.rejection_reason)