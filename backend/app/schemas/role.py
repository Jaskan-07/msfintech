"""
Role Schemas
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleResponse(RoleCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
