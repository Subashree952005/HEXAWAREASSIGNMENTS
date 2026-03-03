from typing import Optional
from pydantic import BaseModel
from app.models.asset import AssetType
from app.models.asset_request import RequestStatus


class AssetRequestCreate(BaseModel):
    asset_type: AssetType
    reason: str


class AssetRequestApprove(BaseModel):
    asset_id: int   # The specific asset to assign after approval


class AssetRequestReject(BaseModel):
    rejection_reason: str


class AssetRequestOut(BaseModel):
    id: int
    employee_id: int
    asset_type: AssetType
    reason: str
    status: RequestStatus
    approved_by: Optional[int]
    rejection_reason: Optional[str]

    class Config:
        from_attributes = True