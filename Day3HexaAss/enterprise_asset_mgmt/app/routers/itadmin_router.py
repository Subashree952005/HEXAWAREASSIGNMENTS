from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.rbac import require_it_admin
from app.services.asset_service import AssetService
from app.services.assignment_service import AssignmentService
from app.services.request_service import RequestService
from app.schemas.asset_schema import AssetCreate, AssetUpdate, AssetOut
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn, AssignmentOut
from app.schemas.request_schema import AssetRequestApprove, AssetRequestReject, AssetRequestOut
from app.models.asset import AssetStatus, AssetType
from app.models.asset_request import RequestStatus
from app.core.pagination import PaginationParams, PaginatedResponse
from app.models.user import User

router = APIRouter(prefix="/itadmin", tags=["IT Admin"], dependencies=[Depends(require_it_admin)])


# ─── Asset CRUD ────────────────────────────────────────────────────────────────

@router.post("/assets", response_model=AssetOut, status_code=201)
async def create_asset(data: AssetCreate, db: AsyncSession = Depends(get_db)):
    return await AssetService(db).create_asset(data)


@router.get("/assets", response_model=PaginatedResponse[AssetOut])
async def list_assets(
    params: PaginationParams = Depends(),
    status: Optional[AssetStatus] = Query(None),
    asset_type: Optional[AssetType] = Query(None),
    department_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await AssetService(db).list_assets(params, status, asset_type, department_id, search)


@router.get("/assets/{asset_id}", response_model=AssetOut)
async def get_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    return await AssetService(db).get_asset(asset_id)


@router.patch("/assets/{asset_id}", response_model=AssetOut)
async def update_asset(asset_id: int, data: AssetUpdate, db: AsyncSession = Depends(get_db)):
    return await AssetService(db).update_asset(asset_id, data)


@router.delete("/assets/{asset_id}", status_code=204)
async def delete_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    await AssetService(db).delete_asset(asset_id)


# ─── Assignments ───────────────────────────────────────────────────────────────

@router.post("/assignments", response_model=AssignmentOut, status_code=201)
async def assign_asset(
    data: AssignmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_it_admin),
):
    return await AssignmentService(db).assign_asset(data, current_user.id)


@router.get("/assignments", response_model=PaginatedResponse[AssignmentOut])
async def list_assignments(params: PaginationParams = Depends(), db: AsyncSession = Depends(get_db)):
    return await AssignmentService(db).list_assignments(params)


@router.post("/assignments/{assignment_id}/return", response_model=AssignmentOut)
async def return_asset(assignment_id: int, data: AssignmentReturn, db: AsyncSession = Depends(get_db)):
    return await AssignmentService(db).return_asset(assignment_id, data)


# ─── Requests ──────────────────────────────────────────────────────────────────

@router.get("/requests", response_model=PaginatedResponse[AssetRequestOut])
async def list_requests(
    params: PaginationParams = Depends(),
    status: Optional[RequestStatus] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await RequestService(db).list_requests(params, status)


@router.post("/requests/{req_id}/approve")
async def approve_request(
    req_id: int,
    data: AssetRequestApprove,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_it_admin),
):
    return await RequestService(db).approve_request(req_id, data, current_user.id)


@router.post("/requests/{req_id}/reject", response_model=AssetRequestOut)
async def reject_request(
    req_id: int,
    data: AssetRequestReject,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_it_admin),
):
    return await RequestService(db).reject_request(req_id, data, current_user.id)