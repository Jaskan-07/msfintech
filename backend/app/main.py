"""
Economic Indicators Dashboard - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Economic Indicators Dashboard with Authentication",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "economic-indicators-api"}


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Economic Indicators Dashboard API",
        "docs": "/docs",
        "version": "1.0.0"
    }
