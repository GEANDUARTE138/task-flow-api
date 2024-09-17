"""
This module defines the API endpoints for managing projects.

Endpoints:
    - create_project_endpoint: Creates a new project.
    - get_project_endpoint: Retrieves a project by its unique key.
    - update_project_endpoint: Updates an existing project.
    - list_projects_by_customer: Lists projects for a customer with pagination.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from api.auth import get_api_key
from connector.mysql_connector import MySQLConnector
from schemas.project import (
    PaginatedProjectsResponseDTO,
    ProjectDTO,
    ProjectResponseDTO,
    ProjectUpdateDTO,
)
from services.project import ProjectService


router = APIRouter()


@router.post(
    "/project",
    status_code=201,
    response_model=ProjectResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def create_project_endpoint(
    request: Request, dto: ProjectDTO
) -> ProjectResponseDTO:
    """
    Endpoint to create a new project.

    Args:
        request (Request): The incoming HTTP request.
        dto (ProjectDTO): The data transfer object containing project details.

    Returns:
        ProjectResponseDTO: The created project.
    """
    with MySQLConnector.session_scope() as session:
        project_service = ProjectService(session)
        return await project_service.create_project(dto)


@router.get(
    "/project/{project_key}",
    status_code=200,
    response_model=ProjectResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def get_project_endpoint(
    project_key: str = Path(..., description="A unique key representing the project")
) -> ProjectResponseDTO:
    """
    Endpoint to retrieve a project by its unique key.

    Args:
        project_key (str): The unique key representing the project.

    Returns:
        ProjectResponseDTO: The retrieved project.

    Raises:
        HTTPException: If the project is not found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        project_service = ProjectService(session)

        project = await project_service.get_project(project_key)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project


@router.put(
    "/project/{project_key}",
    status_code=200,
    response_model=ProjectResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def update_project_endpoint(
    dto: ProjectUpdateDTO,
    project_key: str = Path(..., description="A unique key representing the project"),
) -> ProjectResponseDTO:
    """
    Endpoint to update an existing project by its unique key.

    Args:
        dto (ProjectUpdateDTO): The data transfer object containing updated project details.
        project_key (str): The unique key representing the project.

    Returns:
        ProjectResponseDTO: The updated project.

    Raises:
        HTTPException: If the project is not found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        project_service = ProjectService(session)

        updated_project = await project_service.update_project(project_key, dto)
        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return updated_project


@router.get(
    "/projects/{customer_key}",
    status_code=200,
    response_model=PaginatedProjectsResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def list_projects_by_customer(
    customer_key: str = Path(..., description="A unique key representing the customer"),
    include_activities: Optional[bool] = Query(
        False, description="Include activities in the response"
    ),
    status: Optional[str] = Query(
        "open", description="Filter projects by status (open, closed)"
    ),
    due_date: Optional[datetime] = Query(
        None, description="Filter projects by due date"
    ),
    limit: int = Query(100, description="Number of projects to return per page", gt=0),
    page: int = Query(1, description="Page number to return", gt=0),
) -> PaginatedProjectsResponseDTO:
    """
    Endpoint to list projects for a customer with pagination.

    Args:
        customer_key (str): The unique key representing the customer.
        include_activities (Optional[bool]): Whether to include activities in the response.
        status (Optional[str]): Filter projects by status (open, closed).
        due_date (Optional[datetime]): Filter projects by due date.
        limit (int): The number of projects to return per page (default 100).
        page (int): The page number to return (default 1).

    Returns:
        PaginatedProjectsResponseDTO: A paginated response containing the projects.

    Raises:
        HTTPException: If no projects are found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        project_service = ProjectService(session)

        paginated_response = await project_service.list_projects_by_customer(
            customer_key, include_activities, status, due_date, limit, page
        )
        if not paginated_response:
            raise HTTPException(
                status_code=404, detail="No projects found for this customer"
            )

        return paginated_response
