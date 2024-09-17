"""
This module sets up and includes all the API routes for the FastAPI application.

It imports route modules for activities, customers, health checks, and projects,
and includes them in the main API router.
"""

from fastapi import APIRouter
from api.routes import activity, customer, health, project

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])

router.include_router(
    customer.router,
    tags=["customers"],
)

router.include_router(
    project.router,
    tags=["projects"],
)

router.include_router(
    activity.router,
    tags=["activities"],
)
