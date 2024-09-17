"""
This module defines the ActivityService class, which provides methods for 
creating, retrieving, and updating activities in the task flow system.

Classes:
    - ActivityService: A service class that manages activities, including their creation, retrieval, and updates.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.activity_repository import ActivityRepository
from repositories.project_repository import ProjectRepository
from schemas.activity import ActivityDTO, ActivityResponseDTO
from services.base import BaseService

class ActivityService(BaseService):
    """
    Service class for managing activities in the task flow system.

    Attributes:
        activity_repository (ActivityRepository): Repository for accessing and managing activity data.
        project_repository (ProjectRepository): Repository for accessing and managing project data.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the ActivityService with repositories for activity and project management.

        Args:
            session (Session): SQLAlchemy session for database interactions.
        """
        super().__init__(__name__)
        self.activity_repository = ActivityRepository(session)
        self.project_repository = ProjectRepository(session)

    async def create_activity(self, dto: ActivityDTO) -> ActivityResponseDTO:
        """
        Create a new activity and associate it with a project.

        Args:
            dto (ActivityDTO): Data transfer object containing the details of the activity to be created.

        Returns:
            ActivityResponseDTO: The response data for the created activity.

        Raises:
            HTTPException: If the project associated with the activity is not found.
        """
        try:
            self.logger.info("Starting create_activity")

            project = await self.project_repository.get_by_key(dto.project_key)
            if not project:
                self.logger.error("Project not found", {"project_key": dto.project_key})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found"
                )

            new_activity = await self.activity_repository.create(
                dto.description, dto.due_date, project
            )

            self.logger.info("Activity created", {"activity_key": new_activity.activity_key})

            self.activity_repository.commit()

            response_data = ActivityResponseDTO.model_validate(
                {
                    "activity_key": new_activity.activity_key,
                    "project_key": project.project_key,
                    "description": new_activity.description,
                    "status": new_activity.status.enumerator,
                    "due_date": new_activity.due_date,
                    "created_at": new_activity.created_at,
                    "updated_at": new_activity.updated_at,
                }
            )

            self.logger.info("create_activity completed successfully")

            return response_data

        except Exception as e:
            self.logger.error("An error occurred in create_activity", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def get_activity(self, activity_key: str) -> ActivityResponseDTO:
        """
        Retrieve an activity by its unique key.

        Args:
            activity_key (str): The unique key representing the activity.

        Returns:
            ActivityResponseDTO: The response data for the retrieved activity, or None if not found.
        """
        try:
            self.logger.info(f"Starting get_activity with activity_key: {activity_key}")

            activity = await self.activity_repository.get_by_key(activity_key)
            if not activity:
                self.logger.warning(f"Activity not found for key: {activity_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Activity not found"
                )

            response_data = ActivityResponseDTO.model_validate(
                {
                    "activity_key": activity.activity_key,
                    "project_key": activity.project.project_key,
                    "description": activity.description,
                    "status": activity.status.enumerator,
                    "due_date": activity.due_date,
                    "created_at": activity.created_at,
                    "updated_at": activity.updated_at,
                }
            )

            self.logger.info(f"get_activity successfully retrieved activity_key: {activity_key}")

            return response_data
        
        except Exception as e:
            self.logger.error("An error occurred in get_activity", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def update_activity(
        self, activity_key: str, dto: ActivityDTO
    ) -> ActivityResponseDTO:
        """
        Update an existing activity by its unique key.

        Args:
            activity_key (str): The unique key representing the activity.
            dto (ActivityDTO): Data transfer object containing the updated activity details.

        Returns:
            ActivityResponseDTO: The response data for the updated activity, or None if not found.
        """
        try:
            self.logger.info(f"Starting update_activity with activity_key: {activity_key}")

            activity = await self.activity_repository.get_by_key(activity_key)
            if not activity:
                self.logger.warning(f"Activity not found for key: {activity_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Activity not found"
                )

            updated_activity = await self.activity_repository.update(
                activity, dto.description, dto.status, dto.due_date
            )

            self.activity_repository.commit()

            response_data = ActivityResponseDTO.model_validate(
                {
                    "activity_key": updated_activity.activity_key,
                    "project_key": updated_activity.project.project_key,
                    "description": updated_activity.description,
                    "status": updated_activity.status.enumerator,
                    "due_date": updated_activity.due_date,
                    "created_at": updated_activity.created_at,
                    "updated_at": updated_activity.updated_at,
                }
            )

            self.logger.info(f"update_activity successfully updated activity_key: {activity_key}")

            return response_data

        except Exception as e:
            self.logger.error("An error occurred in update_activity", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )
