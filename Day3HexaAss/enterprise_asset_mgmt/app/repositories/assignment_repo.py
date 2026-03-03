from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.asset_assignment import AssetAssignment
from app.schemas.assignment_schema import AssignmentCreate, AssignmentReturn


class AssignmentRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AssignmentCreate, assigned_by: int) -> AssetAssignment:
        assignment = AssetAssignment(
            asset_id=data.asset_id,
            user_id=data.user_id,
            assigned_by=assigned_by,
            assigned_date=data.assigned_date,
            notes=data.notes,
            is_active=True,
        )
        self.db.add(assignment)
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment

    async def get_by_id(self, assignment_id: int) -> Optional[AssetAssignment]:
        result = await self.db.execute(
            select(AssetAssignment).where(AssetAssignment.id == assignment_id)
        )
        return result.scalar_one_or_none()

    async def get_active_by_asset(self, asset_id: int) -> Optional[AssetAssignment]:
        result = await self.db.execute(
            select(AssetAssignment).where(
                AssetAssignment.asset_id == asset_id,
                AssetAssignment.is_active == True,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> List[AssetAssignment]:
        result = await self.db.execute(
            select(AssetAssignment).where(
                AssetAssignment.user_id == user_id,
                AssetAssignment.is_active == True,
            )
        )
        return result.scalars().all()

    async def get_all(self, offset: int = 0, limit: int = 20) -> tuple[List[AssetAssignment], int]:
        count = (await self.db.execute(select(func.count()).select_from(AssetAssignment))).scalar()
        result = await self.db.execute(select(AssetAssignment).offset(offset).limit(limit))
        return result.scalars().all(), count

    async def return_asset(self, assignment: AssetAssignment, data: AssignmentReturn) -> AssetAssignment:
        assignment.returned_date = data.returned_date
        assignment.condition_on_return = data.condition_on_return
        assignment.notes = data.notes
        assignment.is_active = False
        await self.db.flush()
        await self.db.refresh(assignment)
        return assignment