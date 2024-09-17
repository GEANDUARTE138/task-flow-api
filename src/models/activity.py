"""
This module defines the Activity model for managing activities in the task flow system.

Classes:
    - Activity: A SQLAlchemy model that represents an activity, including attributes for activity key, project, status, due date, and timestamps.
"""

from datetime import UTC, datetime
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.activity_status import ActivityStatus
from models.base import Base
from models.project import Project



class Activity(Base):
    """
    SQLAlchemy model for representing an activity in the task flow system.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        __table_args__ (dict): Additional table options, such as schema.
        id (Column): The primary key of the activity.
        activity_key (Column): A unique key representing the activity.
        project_id (Column): A foreign key referring to the project associated with the activity.
        status_id (Column): A foreign key referring to the status of the activity.
        due_date (Column): The optional due date of the activity.
        description (Column): A description of the activity.
        created_at (Column): The timestamp when the activity was created.
        updated_at (Column): The timestamp when the activity was last updated.
        project (relationship): A relationship to the project associated with the activity.
        status (relationship): A relationship to the activity status.
    """

    __tablename__ = "Activity"
    __table_args__ = {"schema": "task_flow"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_key = Column(String(36), unique=True, nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    status_id = Column(Integer, ForeignKey(ActivityStatus.id), nullable=False)
    due_date = Column(Date)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    project = relationship("Project", back_populates="activities")

    status = relationship(
        "ActivityStatus",
        foreign_keys=[status_id],
        lazy="joined",
    )
