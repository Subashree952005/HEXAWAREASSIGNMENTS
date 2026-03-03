from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.rbac import require_manager
from app.services.asset_service import AssetService
from app.models.asset import AssetStatus, AssetType
from app.schemas.asset_schema import AssetOut
from app.core.pagination import PaginationParams, PaginatedResponse
from app.models.user import User

router = APIRouter(prefix="/manager", tags=["Manager"], dependencies=[Depends(require_manager)])


@router.get("/assets", response_model=PaginatedResponse[AssetOut])
async def view_department_assets(
    params: PaginationParams = Depends(),
    status: Optional[AssetStatus] = Query(None),
    asset_type: Optional[AssetType] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    """Manager sees assets for their own department only."""
    return await AssetService(db).list_assets(
        params,
        status=status,
        asset_type=asset_type,
        department_id=current_user.department_id,
        search=search,
    )


@router.get("/assets/{asset_id}", response_model=AssetOut)
async def get_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    return await AssetService(db).get_asset(asset_id)