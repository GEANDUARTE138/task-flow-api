"""
This module defines the ProjectStatus model for managing the status of projects.

Classes:
    - ProjectStatus: A SQLAlchemy model that represents the status of a project, including fields for ID, enumerator, and creation timestamp.
"""

from datetime import UTC, datetime
from sqlalchemy import Column, DateTime, Integer, String
from models.base import Base

class ProjectStatus(Base):
    """
    SQLAlchemy model for representing the status of a project.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        __table_args__ (dict): Additional table options, such as schema.
        id (Column): The primary key of the project status.
        enumerator (Column): The enumerated value representing the status.
        created_at (Column): The timestamp when the project status was created.
    """
    
    __tablename__ = "ProjectStatus"
    __table_args__ = {"schema": "task_flow"}

    id = Column(Integer, primary_key=True)
    enumerator = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))
