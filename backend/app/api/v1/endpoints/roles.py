"""
Role Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role_data: RoleCreate, db: Session = Depends(get_db)):
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()

    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )

    role = Role(
        name=role_data.name,
        description=role_data.description
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db)
):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role_data.name is not None:
        existing_role = db.query(Role).filter(
            Role.name == role_data.name,
            Role.id != role_id
        ).first()

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )

        role.name = role_data.name

    if role_data.description is not None:
        role.description = role_data.description

    db.commit()
    db.refresh(role)

    return role


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    assigned_user = db.query(User).filter(User.role_id == role_id).first()

    if assigned_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role is assigned to users and cannot be deleted"
        )

    db.delete(role)
    db.commit()

    return {"message": "Role deleted successfully"}
