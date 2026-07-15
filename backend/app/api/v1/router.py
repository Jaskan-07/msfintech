"""
API v1 Router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, roles, user

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    roles.router,
    prefix="/roles",
    tags=["Roles"]
)

api_router.include_router(
    user.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)
