from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.asset_request import AssetRequest, RequestStatus
from app.schemas.request_schema import AssetRequestCreate


class RequestRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AssetRequestCreate, employee_id: int) -> AssetRequest:
        req = AssetRequest(
            employee_id=employee_id,
            asset_type=data.asset_type,
            reason=data.reason,
            status=RequestStatus.PENDING,
        )
        self.db.add(req)
        await self.db.flush()
        await self.db.refresh(req)
        return req

    async def get_by_id(self, req_id: int) -> Optional[AssetRequest]:
        result = await self.db.execute(
            select(AssetRequest).where(AssetRequest.id == req_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
        status: Optional[RequestStatus] = None,
        employee_id: Optional[int] = None,
    ) -> tuple[List[AssetRequest], int]:
        query = select(AssetRequest)
        count_query = select(func.count()).select_from(AssetRequest)

        if status:
            query = query.where(AssetRequest.status == status)
            count_query = count_query.where(AssetRequest.status == status)
        if employee_id:
            query = query.where(AssetRequest.employee_id == employee_id)
            count_query = count_query.where(AssetRequest.employee_id == employee_id)

        total = (await self.db.execute(count_query)).scalar()
        result = await self.db.execute(query.offset(offset).limit(limit))
        return result.scalars().all(), total

    async def approve(self, req: AssetRequest, approved_by: int) -> AssetRequest:
        req.status = RequestStatus.APPROVED
        req.approved_by = approved_by
        await self.db.flush()
        await self.db.refresh(req)
        return req

    async def reject(self, req: AssetRequest, approved_by: int, reason: str) -> AssetRequest:
        req.status = RequestStatus.REJECTED
        req.approved_by = approved_by
        req.rejection_reason = reason
        await self.db.flush()
        await self.db.refresh(req)
        return req