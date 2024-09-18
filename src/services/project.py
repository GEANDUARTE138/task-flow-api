"""
This module defines the ProjectService class, which provides methods for 
creating, retrieving, updating, and listing projects in the task flow system.

Classes:
    - ProjectService: A service class that manages projects, including their creation, retrieval, updates, and listing by customer.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.customer_repository import CustomerRepository
from repositories.project_repository import ProjectRepository
from schemas.project import PaginatedProjectsResponseDTO, ProjectDTO, ProjectResponseDTO
from services.base import BaseService


class ProjectService(BaseService):
    """
    Service class for managing projects in the task flow system.

    Attributes:
        project_repository (ProjectRepository): Repository for accessing and managing project data.
        customer_repository (CustomerRepository): Repository for accessing and managing customer data.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the ProjectService with repositories for project and customer management.

        Args:
            session (Session): SQLAlchemy session for database interactions.
        """
        super().__init__(__name__)
        self.project_repository = ProjectRepository(session)
        self.customer_repository = CustomerRepository(session)

    async def create_project(self, dto: ProjectDTO) -> ProjectResponseDTO:
        """
        Create a new project and associate it with a customer.

        Args:
            dto (ProjectDTO): Data transfer object containing the details of the project to be created.

        Returns:
            ProjectResponseDTO: The response data for the created project.

        Raises:
            HTTPException: If the customer associated with the project is not found.
        """
        try:
            self.logger.info("Starting create_project")

            customer = await self.customer_repository.get_by_key(dto.customer_key)
            if not customer:
                self.logger.error("Customer not found", {"customer_key": dto.customer_key})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )

            new_project = await self.project_repository.create(
                dto.name, customer, dto.due_date
            )

            self.project_repository.commit()

            response_data = ProjectResponseDTO.model_validate(
                {
                    "project_key": new_project.project_key,
                    "name": new_project.name,
                    "status": new_project.status.enumerator,
                    "customer_key": customer.customer_key,
                    "due_date": new_project.due_date,
                    "created_at": new_project.created_at,
                    "updated_at": new_project.updated_at,
                }
            )

            self.logger.info("create_project completed successfully")

            return response_data


        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            self.logger.error("An error occurred in create_project", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def get_project(self, project_key: str) -> ProjectResponseDTO:
        """
        Retrieve a project by its unique key.

        Args:
            project_key (str): The unique key representing the project.

        Returns:
            ProjectResponseDTO: The response data for the retrieved project, or None if not found.
        """
        try:
            self.logger.info(f"Starting get_project with project_key: {project_key}")

            project = await self.project_repository.get_by_key(project_key)
            if not project:
                self.logger.warning(f"Project not found for key: {project_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found"
                )

            response_data = ProjectResponseDTO.model_validate(
                {
                    "project_key": project.project_key,
                    "name": project.name,
                    "status": project.status.enumerator,
                    "customer_key": project.customer.customer_key,
                    "due_date": project.due_date,
                    "created_at": project.created_at,
                    "updated_at": project.updated_at,
                }
            )

            self.logger.info(f"get_project successfully retrieved project_key: {project_key}")

            return response_data

        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            self.logger.error("An error occurred in get_project", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def update_project(
        self, project_key: str, dto: ProjectDTO
    ) -> ProjectResponseDTO:
        """
        Update an existing project by its unique key.

        Args:
            project_key (str): The unique key representing the project.
            dto (ProjectDTO): Data transfer object containing the updated project details.

        Returns:
            ProjectResponseDTO: The response data for the updated project, or None if not found.
        """
        try:
            self.logger.info(f"Starting update_project with project_key: {project_key}")

            project = await self.project_repository.get_by_key(project_key)
            if not project:
                self.logger.warning(f"Project not found for key: {project_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found"
                )

            updated_project = await self.project_repository.update(
                project, dto.name, dto.status, dto.due_date
            )

            self.project_repository.commit()

            response_data = ProjectResponseDTO.model_validate(
                {
                    "project_key": updated_project.project_key,
                    "name": updated_project.name,
                    "status": updated_project.status.enumerator,
                    "customer_key": updated_project.customer.customer_key,
                    "due_date": updated_project.due_date,
                    "created_at": updated_project.created_at,
                    "updated_at": updated_project.updated_at,
                }
            )

            self.logger.info(f"update_project successfully updated project_key: {project_key}")

            return response_data

        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            self.logger.error("An error occurred in update_project", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def list_projects_by_customer(
        self,
        customer_key: str,
        include_activities: bool,
        status: str,
        due_date: Optional[datetime],
        limit: int,
        page: int,
    ) -> PaginatedProjectsResponseDTO:
        """
        List projects by customer, with optional filtering by status and due date.

        Args:
            customer_key (str): The unique key representing the customer.
            include_activities (bool): Whether to include activities in the response.
            status (str): Filter projects by status.
            due_date (Optional[datetime]): Filter projects by due date.
            limit (int): Number of projects to return per page.
            page (int): The page number to return.

        Returns:
            PaginatedProjectsResponseDTO: A paginated response containing the projects.

        Raises:
            HTTPException: If the customer is not found.
        """
        try:
            self.logger.info(f"Starting list_projects_by_customer with customer_key: {customer_key}")

            customer = await self.customer_repository.get_by_key(customer_key)
            if not customer:
                self.logger.error(f"Customer not found for key: {customer_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )

            total_items = await self.project_repository.count_projects_by_customer(
                customer.id, status, due_date
            )

            total_pages = (total_items + limit - 1) // limit

            projects = await self.project_repository.list_projects_by_customer(
                customer.id, status, due_date, limit, page
            )

            project_responses = []
            for project in projects:
                project_data = {
                    "project_key": project.project_key,
                    "name": project.name,
                    "status": project.status.enumerator,
                    "customer_key": customer.customer_key,
                    "due_date": project.due_date,
                    "created_at": project.created_at,
                    "updated_at": project.updated_at,
                }

                if include_activities:
                    project_data["activities"] = [
                        {
                            "activity_key": activity.activity_key,
                            "description": activity.description,
                            "status": activity.status.enumerator,
                            "due_date": activity.due_date,
                            "created_at": activity.created_at,
                            "updated_at": activity.updated_at,
                        }
                        for activity in project.activities
                    ]

                project_responses.append(ProjectResponseDTO.model_validate(project_data))

            self.logger.info(f"list_projects_by_customer successfully retrieved projects for customer_key: {customer_key}")

            return PaginatedProjectsResponseDTO(
                projects=project_responses,
                total_items=total_items,
                total_pages=total_pages,
                current_page=page,
                limit=limit,
            )


        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            self.logger.error("An error occurred in list_projects_by_customer", {"error": str(e)})
            raise HTTPException(
                status_code=500,
                detail="An internal error occurred"
            )


