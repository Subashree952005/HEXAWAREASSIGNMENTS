from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.asset_repo import AssetRepo
from app.repositories.user_repo import UserRepo
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from app.models.asset import AssetStatus, AssetType
from app.core.pagination import PaginationParams, PaginatedResponse


class AssetService:
    def __init__(self, db: AsyncSession):
        self.repo = AssetRepo(db)

    async def create_asset(self, data: AssetCreate):
        existing = await self.repo.get_by_tag(data.asset_tag)
        if existing:
            raise HTTPException(status_code=400, detail=f"Asset tag '{data.asset_tag}' already exists")
        return await self.repo.create(data)

    async def get_asset(self, asset_id: int):
        asset = await self.repo.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset

    async def list_assets(
        self,
        params: PaginationParams,
        status: Optional[AssetStatus] = None,
        asset_type: Optional[AssetType] = None,
        department_id: Optional[int] = None,
        search: Optional[str] = None,
    ):
        items, total = await self.repo.get_all(
            offset=params.offset,
            limit=params.size,
            status=status,
            asset_type=asset_type,
            department_id=department_id,
            search=search,
        )
        return PaginatedResponse.create(items, total, params)

    async def update_asset(self, asset_id: int, data: AssetUpdate):
        asset = await self.get_asset(asset_id)
        return await self.repo.update(asset, data)

    async def delete_asset(self, asset_id: int):
        asset = await self.get_asset(asset_id)
        if asset.status == AssetStatus.ASSIGNED:
            raise HTTPException(status_code=400, detail="Cannot delete an assigned asset")
        return await self.repo.soft_delete(asset)