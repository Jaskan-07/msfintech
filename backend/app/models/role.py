"""
Role model and role constants.
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class Role(Base):
    __tablename__ = "ms_role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class RoleName(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    MANAGER = "manager"
    INACTIVE = "inactive"


ACTIVE_ROLES = frozenset({RoleName.ADMIN, RoleName.ANALYST, RoleName.MANAGER})
