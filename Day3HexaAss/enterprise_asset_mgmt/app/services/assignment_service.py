from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.repositories.assignment_repo import AssignmentRepo
from app.repositories.asset_repo import AssetRepo
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn
from app.models.asset import AssetStatus
from app.core.pagination import PaginationParams, PaginatedResponse


class AssignmentService:
    def __init__(self, db: AsyncSession):
        self.repo = AssignmentRepo(db)
        self.asset_repo = AssetRepo(db)

    async def assign_asset(self, data: AssignmentCreate, assigned_by: int):
        asset = await self.asset_repo.get_by_id(data.asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        if asset.status != AssetStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail=f"Asset is not available. Current status: {asset.status}")

        existing = await self.repo.get_active_by_asset(data.asset_id)
        if existing:
            raise HTTPException(status_code=400, detail="Asset already has an active assignment")

        assignment = await self.repo.create(data, assigned_by)
        await self.asset_repo.update_status(asset, AssetStatus.ASSIGNED)
        return assignment

    async def return_asset(self, assignment_id: int, data: AssignmentReturn):
        assignment = await self.repo.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        if not assignment.is_active:
            raise HTTPException(status_code=400, detail="Asset already returned")

        updated = await self.repo.return_asset(assignment, data)
        asset = await self.asset_repo.get_by_id(assignment.asset_id)
        await self.asset_repo.update_status(asset, AssetStatus.AVAILABLE)
        return updated

    async def get_user_assignments(self, user_id: int):
        return await self.repo.get_by_user(user_id)

    async def list_assignments(self, params: PaginationParams):
        items, total = await self.repo.get_all(offset=params.offset, limit=params.size)
        return PaginatedResponse.create(items, total, params)