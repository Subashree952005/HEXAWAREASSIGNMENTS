from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.asset import Asset, AssetStatus, AssetType
from app.schemas.asset_schema import AssetCreate, AssetUpdate


class AssetRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AssetCreate) -> Asset:
        asset = Asset(**data.model_dump())
        self.db.add(asset)
        await self.db.flush()
        await self.db.refresh(asset)
        return asset

    async def get_by_id(self, asset_id: int) -> Optional[Asset]:
        result = await self.db.execute(
            select(Asset).where(Asset.id == asset_id, Asset.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_by_tag(self, tag: str) -> Optional[Asset]:
        result = await self.db.execute(
            select(Asset).where(Asset.asset_tag == tag, Asset.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
        status: Optional[AssetStatus] = None,
        asset_type: Optional[AssetType] = None,
        department_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[List[Asset], int]:
        query = select(Asset).where(Asset.is_deleted == False)
        count_query = select(func.count()).select_from(Asset).where(Asset.is_deleted == False)

        if status:
            query = query.where(Asset.status == status)
            count_query = count_query.where(Asset.status == status)
        if asset_type:
            query = query.where(Asset.asset_type == asset_type)
            count_query = count_query.where(Asset.asset_type == asset_type)
        if department_id:
            query = query.where(Asset.department_id == department_id)
            count_query = count_query.where(Asset.department_id == department_id)
        if search:
            query = query.where(Asset.asset_tag.ilike(f"%{search}%"))
            count_query = count_query.where(Asset.asset_tag.ilike(f"%{search}%"))

        total = (await self.db.execute(count_query)).scalar()
        result = await self.db.execute(query.offset(offset).limit(limit))
        return result.scalars().all(), total

    async def get_available_by_type(self, asset_type: AssetType) -> List[Asset]:
        result = await self.db.execute(
            select(Asset).where(
                Asset.asset_type == asset_type,
                Asset.status == AssetStatus.AVAILABLE,
                Asset.is_deleted == False,
            )
        )
        return result.scalars().all()

    async def update(self, asset: Asset, data: AssetUpdate) -> Asset:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(asset, field, value)
        await self.db.flush()
        await self.db.refresh(asset)
        return asset

    async def update_status(self, asset: Asset, status: AssetStatus) -> Asset:
        asset.status = status
        await self.db.flush()
        return asset

    async def soft_delete(self, asset: Asset) -> Asset:
        asset.is_deleted = True
        await self.db.flush()
        return asset