"""
This module defines the health check endpoint for the FastAPI application.

It includes a simple GET route to check the status of the application.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("", status_code=200)
async def ping_health_check() -> dict:
    """
    Health check endpoint that returns the status of the application.

    Returns:
        dict: A JSON object containing the status of the application.
    """
    return {"status": "ok"}
