"""
This module contains Data Transfer Objects (DTOs) for managing Customer data
in a FastAPI application.

DTOs:
    - CustomerDTO: Used for creating a new customer.
    - CustomerUpdateDTO: Used for updating an existing customer.
    - CustomerResponseDTO: Used for responding with customer data, including status and timestamps.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CustomerDTO(BaseModel):
    """
    Data Transfer Object for creating a new customer.

    Attributes:
        - name: The name of the customer (min length 1, max length 255).
        - email: The email of the customer (min length 1, max length 255).
    """

    name: str = Field(..., min_length=1, max_length=255, description="Nome do cliente")
    email: str = Field(
        ..., min_length=1, max_length=255, description="Email do cliente"
    )

    model_config = ConfigDict(from_attributes=True)


class CustomerUpdateDTO(BaseModel):
    """
    Data Transfer Object for updating an existing customer.

    Attributes:
        - name: The optional name of the customer (min length 1, max length 255).
        - email: The optional email of the customer (min length 1, max length 255).
        - status: The optional status of the customer (active, inactive, suspended).
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Nome do cliente"
    )
    email: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Email do cliente"
    )
    status: Optional[str] = Field(
        None, description="Status do cliente (active, inactive, suspended)"
    )

    model_config = ConfigDict(from_attributes=True)


class CustomerResponseDTO(BaseModel):
    """
    Data Transfer Object for responding with customer data.

    Attributes:
        - customer_key: A unique key identifying the customer.
        - name: The name of the customer.
        - email: The email of the customer.
        - status: The current status of the customer.
        - created_at: The timestamp when the customer was created.
        - updated_at: The timestamp when the customer was last updated.
    """

    customer_key: str = Field(..., description="Chave única para o cliente")
    name: str = Field(..., description="Nome do cliente")
    email: str = Field(..., description="Email do cliente")
    status: str = Field(..., description="Status do cliente")
    created_at: Optional[datetime] = Field(
        None, description="Data e hora de criação do cliente"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Data e hora da última atualização do cliente"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )