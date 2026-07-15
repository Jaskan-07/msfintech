"""
FastAPI dependencies for RBAC.
"""
from typing import Callable

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import ACTIVE_ROLES, RoleName
from app.models.user import User


def get_current_user(
    x_username: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not x_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    user = db.query(User).filter(User.username == x_username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    user_role = RoleName(user.role.name)
    if user_role not in ACTIVE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return user


def require_roles(*allowed_roles: RoleName) -> Callable:
    allowed = frozenset(allowed_roles)

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        user_role = RoleName(current_user.role.name)
        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return dependency
