"""
This module defines the Project model for managing projects in the task flow system.

Classes:
    - Project: A SQLAlchemy model that represents a project, including attributes for project key, customer, status, name, due date, and timestamps.
"""

from datetime import UTC, datetime
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.customer import Customer
from models.project_status import ProjectStatus

class Project(Base):
    """
    SQLAlchemy model for representing a project in the task flow system.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        __table_args__ (dict): Additional table options, such as schema.
        id (Column): The primary key of the project.
        project_key (Column): A unique key representing the project.
        customer_id (Column): A foreign key referring to the customer who owns the project.
        status_id (Column): A foreign key referring to the status of the project.
        name (Column): The name of the project.
        due_date (Column): The optional due date of the project.
        created_at (Column): The timestamp when the project was created.
        updated_at (Column): The timestamp when the project was last updated.
        activities (relationship): A relationship to the activities associated with the project.
        customer (relationship): A relationship to the customer who owns the project.
        status (relationship): A relationship to the project status.
    """

    __tablename__ = "Project"
    __table_args__ = {"schema": "task_flow"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_key = Column(String(36), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    status_id = Column(Integer, ForeignKey(ProjectStatus.id), nullable=False)
    name = Column(String(100), nullable=False)

    due_date = Column(Date)

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    activities = relationship("Activity", back_populates="project")

    customer = relationship("Customer", back_populates="projects")

    status = relationship(
        "ProjectStatus",
        foreign_keys=[status_id],
        lazy="joined",
    )
