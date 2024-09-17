"""
This module contains Data Transfer Objects (DTOs) for managing Project data
in a FastAPI application.

DTOs:
    - ProjectDTO: Used for creating a new project.
    - ProjectUpdateDTO: Used for updating an existing project.
    - ProjectResponseDTO: Used for responding with project data, including status and timestamps.
    - PaginatedProjectsResponseDTO: Used for paginated responses of projects.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProjectDTO(BaseModel):
    """
    Data Transfer Object for creating a new project.

    Attributes:
        - name: The name of the project (min length 1, max length 255).
        - customer_key: A unique key identifying the customer related to the project.
        - due_date: The optional due date for the project.
    """

    name: str = Field(..., min_length=1, max_length=255, description="Nome do projeto")
    customer_key: str = Field(..., description="Chave única para o cliente")
    due_date: Optional[datetime] = Field(
        None, description="Data de conclusão do projeto"
    )

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdateDTO(BaseModel):
    """
    Data Transfer Object for updating an existing project.

    Attributes:
        - name: The optional name of the project (min length 1, max length 255).
        - status: The optional current status of the project (open, closed).
        - due_date: The optional due date for the project.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Nome do projeto"
    )
    status: Optional[str] = Field(None, description="Status do projeto (open, closed)")
    due_date: Optional[datetime] = Field(
        None, description="Data de conclusão do projeto"
    )

    model_config = ConfigDict(from_attributes=True)


class ProjectResponseDTO(BaseModel):
    """
    Data Transfer Object for responding with project data.

    Attributes:
        - project_key: A unique key identifying the project.
        - name: The name of the project.
        - status: The current status of the project (open, closed).
        - customer_key: A unique key identifying the customer related to the project.
        - due_date: The optional due date for the project.
        - created_at: The timestamp when the project was created.
        - updated_at: The timestamp when the project was last updated.
    """

    project_key: str = Field(..., description="Chave única do projeto")
    name: str = Field(..., description="Nome do projeto")
    status: str = Field(..., description="Status do projeto (open, closed)")
    customer_key: str = Field(
        ..., description="Chave do cliente relacionado ao projeto"
    )
    due_date: Optional[datetime] = Field(
        None, description="Data de conclusão do projeto"
    )
    created_at: Optional[datetime] = Field(
        None, description="Data de criação do projeto"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Data da última atualização do projeto"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )


class PaginatedProjectsResponseDTO(BaseModel):
    """
    Data Transfer Object for responding with a paginated list of projects.

    Attributes:
        - projects: The list of paginated projects.
        - total_items: The total number of available projects.
        - total_pages: The total number of pages.
        - current_page: The current page number.
        - limit: The number of projects per page.
    """
    
    projects: List[ProjectResponseDTO] = Field(
        ..., description="Lista de projetos paginados"
    )
    total_items: int = Field(..., description="Total de projetos disponíveis")
    total_pages: int = Field(..., description="Número total de páginas")
    current_page: int = Field(..., description="Página atual")
    limit: int = Field(..., description="Número de projetos por página")
