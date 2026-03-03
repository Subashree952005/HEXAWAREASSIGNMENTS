from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.asset_service import AssetService
from app.models.asset import AssetStatus, AssetType
from app.core.pagination import PaginationParams


class ManagerController:
    def __init__(self, db: AsyncSession):
        self.asset_svc = AssetService(db)

    async def list_department_assets(
        self,
        department_id: int,
        params: PaginationParams,
        status: Optional[AssetStatus] = None,
        asset_type: Optional[AssetType] = None,
        search: Optional[str] = None,
    ):
        return await self.asset_svc.list_assets(
            params,
            status=status,
            asset_type=asset_type,
            department_id=department_id,
            search=search,
        )

    async def get_asset(self, asset_id: int):
        return await self.asset_svc.get_asset(asset_id)