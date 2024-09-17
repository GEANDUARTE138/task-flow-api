"""
This module contains the ProjectRepository class for managing CRUD operations 
on the Project model.

Classes:
    - ProjectRepository: Handles the creation, retrieval, and update of projects, 
      and provides methods for counting and listing projects by customer.
"""

import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from models.customer import Customer
from models.project import Project
from models.project_status import ProjectStatus
from repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository):
    """
    Repository class for managing Project model CRUD operations.

    This class provides methods for creating a new project, retrieving a project by key,
    updating a project, counting projects by customer, and listing projects by customer.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the ProjectRepository with a database session.

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
        """
        super().__init__(session=session, class_name=__name__)

    async def create(
        self, name: str, customer: Customer, due_date: Optional[datetime] = None
    ) -> Project:
        """
        Create a new project in the database.

        Args:
            name (str): The name of the project.
            customer (Customer): The customer associated with the project.
            due_date (Optional[datetime]): The optional due date for the project.

        Returns:
            Project: The newly created Project object.
        """
        new_project = Project()
        new_project.project_key = str(uuid.uuid4())
        new_project.status = await self.get_enumerator(ProjectStatus, "open")
        new_project.customer = customer
        new_project.name = name

        if due_date:
            new_project.due_date = due_date

        self.add(new_project)
        return new_project

    async def get_by_key(self, project_key: str):
        """
        Retrieve a project from the database by its unique key.

        Args:
            project_key (str): The unique key identifying the project.

        Returns:
            Project: The Project object if found, otherwise None.
        """
        project = self.query(Project).filter_by(project_key=project_key).first()

        return project

    async def update(
        self,
        project: Project,
        name: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[datetime] = None,
    ) -> Project:
        """
        Update an existing project with new information.

        Args:
            project (Project): The project to be updated.
            name (Optional[str]): The new name for the project (if provided).
            status (Optional[str]): The new status for the project (if provided).
            due_date (Optional[datetime]): The new due date for the project (if provided).

        Returns:
            Project: The updated Project object.
        """
        if name:
            project.name = name
        if due_date:
            project.due_date = due_date
        if status:
            new_status = await self.get_enumerator(ProjectStatus, status)
            if new_status:
                project.status = new_status

        return project

    async def count_projects_by_customer(
        self, customer_id: int, status: str, due_date: Optional[datetime]
    ) -> int:
        """
        Count the number of projects for a specific customer, optionally filtering by status and due date.

        Args:
            customer_id (int): The ID of the customer.
            status (str): The status of the projects to count.
            due_date (Optional[datetime]): The optional due date filter.

        Returns:
            int: The total number of projects for the customer that match the criteria.
        """
        query = self.query(Project).filter(Project.customer_id == customer_id)

        if status:
            status_obj = await self.get_enumerator(ProjectStatus, status)
            query = query.filter(Project.status == status_obj)

        if due_date:
            query = query.filter(Project.due_date <= due_date)

        return query.count()

    async def list_projects_by_customer(
        self,
        customer_id: int,
        status: str,
        due_date: Optional[datetime],
        limit: int,
        page: int,
    ) -> List[Project]:
        """
        List projects for a specific customer, optionally filtering by status and due date, with pagination.

        Args:
            customer_id (int): The ID of the customer.
            status (str): The status of the projects to list.
            due_date (Optional[datetime]): The optional due date filter.
            limit (int): The maximum number of projects to return per page.
            page (int): The page number to retrieve.

        Returns:
            List[Project]: A list of projects that match the criteria.
        """
        query = self.query(Project).filter(Project.customer_id == customer_id)

        if status:
            status_obj = await self.get_enumerator(ProjectStatus, status)
            query = query.filter(Project.status == status_obj)

        if due_date:
            query = query.filter(Project.due_date <= due_date)

        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        return query.all()
