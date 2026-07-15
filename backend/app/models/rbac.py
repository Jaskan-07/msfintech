"""
RBAC Models
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base import Base


role_permissions = Table(
    "ms_role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("ms_roles.role_id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("ms_permissions.permission_id"), primary_key=True),
)


class Role(Base):
    """Role model for user access levels"""
    __tablename__ = "ms_roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String(50), nullable=False)

    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
    )


class Permission(Base):
    """Permission model for RBAC capabilities"""
    __tablename__ = "ms_permissions"

    permission_id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(50), nullable=False)
    permission_description = Column(String(255), nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(50), nullable=False)

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions",
    )
