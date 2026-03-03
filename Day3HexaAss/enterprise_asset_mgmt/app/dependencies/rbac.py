from fastapi import Depends, HTTPException, status
from app.services.auth_service import get_current_user
from app.models.user import User, UserRole


def require_roles(*roles: UserRole):
    async def wrapper(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in roles]}"
            )
        return current_user
    return wrapper


# Convenience role dependencies
require_superadmin = require_roles(UserRole.SUPERADMIN)
require_it_admin = require_roles(UserRole.SUPERADMIN, UserRole.IT_ADMIN)
require_manager = require_roles(UserRole.SUPERADMIN, UserRole.IT_ADMIN, UserRole.MANAGER)
require_any = require_roles(*UserRole)