"""
This module contains Data Transfer Objects (DTOs) for managing Activity data
in a FastAPI application.

DTOs:
    - ActivityDTO: Used for creating a new activity.
    - ActivityUpdateDTO: Used for updating an existing activity.
    - ActivityResponseDTO: Used for responding with activity data, including status and timestamps.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ActivityDTO(BaseModel):
    """
    Data Transfer Object for creating a new activity.

    Attributes:
        - description: A brief description of the activity (min length 1).
        - project_key: A unique key identifying the related project.
        - due_date: The optional due date for the activity.
    """

    description: str = Field(..., min_length=1, description="Descrição da atividade")
    project_key: str = Field(
        ..., description="Chave única do projeto relacionado à atividade"
    )
    due_date: Optional[datetime] = Field(
        None, description="Data de conclusão da atividade"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )

class ActivityUpdateDTO(BaseModel):
    """
    Data Transfer Object for updating an existing activity.

    Attributes:
        - project_key: The optional unique key of the related project.
        - description: The optional description of the activity (min length 1).
        - due_date: The optional due date for the activity.
        - status: The optional current status of the activity (not_started, in_progress, completed, blocked).
    """

    project_key: Optional[str] = Field(
        None, description="Chave única do projeto relacionado à atividade"
    )
    description: Optional[str] = Field(
        None, min_length=1, description="Descrição da atividade"
    )
    due_date: Optional[datetime] = Field(
        None, description="Data de conclusão da atividade"
    )
    status: Optional[str] = Field(
        None,
        description="Status da atividade (not_started, in_progress, completed, blocked)",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )

class ActivityResponseDTO(BaseModel):
    """
    Data Transfer Object for responding with activity data.

    Attributes:
        - activity_key: A unique key identifying the activity.
        - project_key: A unique key identifying the related project.
        - description: A description of the activity.
        - status: The current status of the activity.
        - due_date: The optional due date of the activity.
        - created_at: The timestamp when the activity was created.
        - updated_at: The timestamp when the activity was last updated.
    """

    activity_key: str = Field(..., description="Chave única da atividade")
    project_key: str = Field(
        ..., description="Chave única do projeto relacionado à atividade"
    )
    due_date: Optional[datetime] = Field(
        None, description="The optional due date for the activity"
    )
    description: str = Field(..., description="Descrição da atividade")
    status: str = Field(..., description="Status da atividade")
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )