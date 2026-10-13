"""
API v1 Router
"""
from fastapi import APIRouter

# Added "stocks" here at the end of the import statement
from app.api.v1.endpoints import auth, roles, users, stocks
from app.api.v1.endpoints import auth, roles, users, stocks

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
    users.router,
    prefix="/users",
    tags=["Users"]
)

# Added your new Live Market Data router mapping block below
api_router.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["Live Market Data"]
)
api_router.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["Stocks"]
)
