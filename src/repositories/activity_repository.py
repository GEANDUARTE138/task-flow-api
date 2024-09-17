"""
This module contains the ActivityRepository class for managing CRUD operations 
on the Activity model.

Classes:
    - ActivityRepository: Handles the creation, retrieval, and update of activities.
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.activity import Activity
from models.activity_status import ActivityStatus
from models.project import Project
from repositories.base_repository import BaseRepository


class ActivityRepository(BaseRepository):
    """
    Repository class for managing Activity model CRUD operations.

    This class provides methods for creating a new activity, retrieving an activity by key,
    and updating an activity.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the ActivityRepository with a database session.

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
        """
        super().__init__(session=session, class_name=__name__)

    async def create(
        self, description: str, due_date: str, project: Project
    ) -> Activity:
        """
        Create a new activity in the database.

        Args:
            description (str): The description of the activity.
            due_date (str): The due date of the activity.
            project (Project): The project to which the activity belongs.

        Returns:
            Activity: The newly created Activity object.
        """
        new_activity = Activity()
        new_activity.activity_key = str(uuid.uuid4())
        new_activity.status = await self.get_enumerator(ActivityStatus, "not_started")
        new_activity.project = project
        new_activity.description = description
        new_activity.due_date = due_date

        self.add(new_activity)
        return new_activity

    async def get_by_key(self, activity_key: str):
        """
        Retrieve an activity from the database by its unique key.

        Args:
            activity_key (str): The unique key identifying the activity.

        Returns:
            Activity: The Activity object if found, otherwise None.
        """
        project = self.query(Activity).filter_by(activity_key=activity_key).first()

        return project

    async def update(
        self,
        activity: Activity,
        description: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> Activity:
        """
        Update an existing activity with new information.

        Args:
            activity (Activity): The activity to be updated.
            description (Optional[str]): The new description for the activity (if provided).
            status (Optional[str]): The new status for the activity (if provided).
            due_date (Optional[str]): The new due date for the activity (if provided).

        Returns:
            Activity: The updated Activity object.
        """
        if description:
            activity.description = description

        if due_date:
            activity.due_date = due_date
        if status:
            new_status = await self.get_enumerator(ActivityStatus, status)
            if new_status:
                activity.status = new_status

        return activity
