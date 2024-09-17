"""
This module defines the API endpoints for managing activities.

Endpoints:
    - create_activity_endpoint: Creates a new activity.
    - get_activity_endpoint: Retrieves an activity by its unique key.
    - update_activity_endpoint: Updates an existing activity.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from api.auth import get_api_key
from connector.mysql_connector import MySQLConnector
from schemas.activity import ActivityDTO, ActivityResponseDTO, ActivityUpdateDTO
from services.activity import ActivityService

router = APIRouter()

@router.post(
    "/activity",
    status_code=200,
    response_model=ActivityResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def create_activity_endpoint(
    request: Request, dto: ActivityDTO
) -> ActivityResponseDTO:
    """
    Endpoint to create a new activity.

    Args:
        request (Request): The incoming HTTP request.
        dto (ActivityDTO): The data transfer object containing activity details.

    Returns:
        ActivityResponseDTO: The created activity.
    """
    with MySQLConnector.session_scope() as session:
        activity_service = ActivityService(session)
        return await activity_service.create_activity(dto)


@router.get(
    "/activity/{activity_key}",
    status_code=200,
    response_model=ActivityResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def get_activity_endpoint(
    activity_key: str = Path(..., description="A unique key representing the activity")
) -> ActivityResponseDTO:
    """
    Endpoint to retrieve an activity by its unique key.

    Args:
        activity_key (str): The unique key representing the activity.

    Returns:
        ActivityResponseDTO: The retrieved activity.

    Raises:
        HTTPException: If the activity is not found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        activity_service = ActivityService(session)

        activity = await activity_service.get_activity(activity_key)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity


@router.put(
    "/activity/{activity_key}",
    status_code=200,
    response_model=ActivityResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def update_activity_endpoint(
    dto: ActivityUpdateDTO,
    activity_key: str = Path(..., description="A unique key representing the activity"),
) -> ActivityResponseDTO:
    """
    Endpoint to update an existing activity by its unique key.

    Args:
        dto (ActivityUpdateDTO): The data transfer object containing updated activity details.
        activity_key (str): The unique key representing the activity.

    Returns:
        ActivityResponseDTO: The updated activity.

    Raises:
        HTTPException: If the activity is not found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        activity_service = ActivityService(session)

        updated_activity = await activity_service.update_activity(activity_key, dto)
        if not updated_activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return updated_activity
