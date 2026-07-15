"""
RBAC Endpoints
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.rbac import Permission, Role
from app.schemas.rbac import PermissionResponse, RoleResponse

router = APIRouter()


@router.get("/roles", response_model=List[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    """
    List roles with their permissions.
    """
    return (
        db.query(Role)
        .options(selectinload(Role.permissions))
        .order_by(Role.role_id)
        .all()
    )


@router.get("/permissions", response_model=List[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    """
    List available permissions.
    """
    return db.query(Permission).order_by(Permission.permission_id).all()
