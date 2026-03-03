from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import decode_token
from app.repositories.user_repo import user_repo
from app.models.user import RoleEnum
from jose import JWTError

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload.get("sub"))
    except (JWTError, Exception):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(*roles: RoleEnum):
    def wrapper(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Access forbidden: insufficient role")
        return current_user
    return wrapper

def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def require_manager(current_user=Depends(get_current_user)):
    if current_user.role != RoleEnum.MANAGER:
        raise HTTPException(status_code=403, detail="Manager access required")
    return current_user

def require_employee(current_user=Depends(get_current_user)):
    if current_user.role != RoleEnum.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Employee access required")
    return current_user