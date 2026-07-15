from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.rbac import Role
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, UserUpdate

router = APIRouter()


def _query_users(db: Session):
    return db.query(User).options(
        selectinload(User.role).selectinload(Role.permissions)
    )


def _get_user_or_404(user_id: int, db: Session) -> User:
    user = _query_users(db).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def _validate_unique_user_fields(
    db: Session,
    username: str | None = None,
    email: str | None = None,
    user_id: int | None = None,
) -> None:
    filters = []
    if username is not None:
        filters.append(User.username == username)
    if email is not None:
        filters.append(User.email == email)
    if not filters:
        return

    query = db.query(User).filter(or_(*filters))
    if user_id is not None:
        query = query.filter(User.id != user_id)

    existing_user = query.first()
    if existing_user is None:
        return
    if username is not None and existing_user.username == username:
        detail = "Username already registered"
    else:
        detail = "Email already registered"
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def _validate_role(db: Session, role_id: int | None) -> None:
    if role_id is None:
        return
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found",
        )


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _query_users(db).order_by(User.id).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_user_or_404(user_id, db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _validate_unique_user_fields(db, user_data.username, user_data.email)
    _validate_role(db, user_data.role_id)

    viewer_role = db.query(Role).filter(Role.role_name == "Viewer").first()
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=user_data.password,
        role_id=user_data.role_id if user_data.role_id is not None else viewer_role.role_id if viewer_role else None,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return _get_user_or_404(db_user.id, db)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = _get_user_or_404(user_id, db)
    update_data = user_data.model_dump(exclude_unset=True)

    _validate_unique_user_fields(
        db,
        username=update_data.get("username"),
        email=update_data.get("email"),
        user_id=user_id,
    )
    _validate_role(db, update_data.get("role_id"))

    password = update_data.pop("password", None)
    if password is not None:
        db_user.hashed_password = password

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return _get_user_or_404(user_id, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = _get_user_or_404(user_id, db)
    db.delete(db_user)
    db.commit()
