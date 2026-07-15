"""
Admin user endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db.session import get_db
from app.models.role import RoleName
from app.models.user import User
from app.schemas.auth import AdminUserCreate, UserOut

router = APIRouter()


@router.post(
    "/users",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleName.ADMIN))],
)
def create_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=user_data.password,
        role_id=user_data.role_id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get(
    "/users",
    response_model=list[UserOut],
    dependencies=[Depends(require_roles(RoleName.ADMIN))],
)
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .order_by(User.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/users/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(require_roles(RoleName.ADMIN))],
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
