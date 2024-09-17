"""
This module defines the ActivityStatus model for managing the status of activities in the task flow system.

Classes:
    - ActivityStatus: A SQLAlchemy model that represents the status of an activity, including attributes for ID, enumerator, and creation timestamp.
"""

from datetime import UTC, datetime
from sqlalchemy import Column, DateTime, Integer, String
from models.base import Base

class ActivityStatus(Base):
    """
    SQLAlchemy model for representing the status of an activity in the task flow system.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        __table_args__ (dict): Additional table options, such as schema.
        id (Column): The primary key of the activity status.
        enumerator (Column): The enumerated value representing the status.
        created_at (Column): The timestamp when the activity status was created.
    """
    
    __tablename__ = "ActivityStatus"
    __table_args__ = {"schema": "task_flow"}

    id = Column(Integer, primary_key=True)
    enumerator = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))
