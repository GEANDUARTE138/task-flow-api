"""
This module defines the API endpoints for managing customers.

Endpoints:
    - create_customer_endpoint: Creates a new customer.
    - get_customer_endpoint: Retrieves a customer by its unique key.
    - update_customer_endpoint: Updates an existing customer.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from api.auth import get_api_key
from connector.mysql_connector import MySQLConnector
from schemas.customer import CustomerDTO, CustomerResponseDTO, CustomerUpdateDTO
from services.customer import CustomerService


router = APIRouter()


@router.post(
    "/customer",
    status_code=201,
    response_model=CustomerResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def create_customer_endpoint(
    request: Request, dto: CustomerDTO
) -> CustomerResponseDTO:
    """
    Endpoint to create a new customer.

    Args:
        request (Request): The incoming HTTP request.
        dto (CustomerDTO): The data transfer object containing customer details.

    Returns:
        CustomerResponseDTO: The created customer.
    """
    with MySQLConnector.session_scope() as session:
        customer_service = CustomerService(session)
        return await customer_service.create_customer(dto)


@router.get(
    "/customer/{customer_key}",
    status_code=200,
    response_model=CustomerResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def get_customer_endpoint(
    customer_key: str = Path(..., description="A unique key representing the customer")
) -> CustomerResponseDTO:
    """
    Endpoint to retrieve a customer by its unique key.

    Args:
        customer_key (str): The unique key representing the customer.

    Returns:
        CustomerResponseDTO: The retrieved customer.

    Raises:
        HTTPException: If the customer is not found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        customer_service = CustomerService(session)

        customer = await customer_service.get_customer(customer_key)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer


@router.put(
    "/customer/{customer_key}",
    status_code=200,
    response_model=CustomerResponseDTO,
    dependencies=[Depends(get_api_key)],
)
async def update_customer_endpoint(
    dto: CustomerUpdateDTO,
    customer_key: str = Path(..., description="A unique key representing the customer"),
) -> CustomerResponseDTO:
    """
    Endpoint to update an existing customer by its unique key.

    Args:
        dto (CustomerUpdateDTO): The data transfer object containing updated customer details.
        customer_key (str): The unique key representing the customer.

    Returns:
        CustomerResponseDTO: The updated customer.

    Raises:
        HTTPException: If the customer is not found, returns a 404 error.
    """
    with MySQLConnector.session_scope() as session:
        customer_service = CustomerService(session)

        updated_customer = await customer_service.update_customer(customer_key, dto)
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated_customer
