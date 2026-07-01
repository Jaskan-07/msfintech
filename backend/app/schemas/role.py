"""
Role Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(RoleCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True