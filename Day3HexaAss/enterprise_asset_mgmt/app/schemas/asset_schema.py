from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.models.asset import AssetType, AssetStatus


class AssetCreate(BaseModel):
    asset_tag: str
    asset_type: AssetType
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[date] = None
    department_id: Optional[int] = None
    notes: Optional[str] = None


class AssetUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    status: Optional[AssetStatus] = None
    department_id: Optional[int] = None
    notes: Optional[str] = None


class AssetOut(BaseModel):
    id: int
    asset_tag: str
    asset_type: AssetType
    brand: Optional[str]
    model: Optional[str]
    purchase_date: Optional[date]
    status: AssetStatus
    department_id: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True