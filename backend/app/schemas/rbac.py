"""
RBAC Schemas
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class PermissionResponse(BaseModel):
    permission_id: int
    permission_name: str
    permission_description: str

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    modified_at: datetime
    modified_by: str
    permissions: List[PermissionResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
