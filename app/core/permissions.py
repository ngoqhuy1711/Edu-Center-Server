from fastapi import Depends, HTTPException, status
from app.api.v1.endpoints.auth import get_current_user
from app.models import User
from sqlmodel import Session, select
from app.db.session import get_session

def require_role(*roles):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return user
    return role_checker 