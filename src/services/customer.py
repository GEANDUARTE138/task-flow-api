"""
This module defines the CustomerService class, which provides methods for 
creating, retrieving, and updating customers in the task flow system.

Classes:
    - CustomerService: A service class that manages customers, including their creation, retrieval, and updates.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.customer_repository import CustomerRepository
from schemas.customer import CustomerDTO, CustomerResponseDTO
from services.base import BaseService


class CustomerService(BaseService):
    """
    Service class for managing customers in the task flow system.

    Attributes:
        customer_repository (CustomerRepository): Repository for accessing and managing customer data.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the CustomerService with a repository for customer management.

        Args:
            session (Session): SQLAlchemy session for database interactions.
        """
        super().__init__(__name__)
        self.customer_repository = CustomerRepository(session)

    async def create_customer(self, dto: CustomerDTO) -> CustomerResponseDTO:
        """
        Create a new customer.

        Args:
            dto (CustomerDTO): Data transfer object containing the details of the customer to be created.

        Returns:
            CustomerResponseDTO: The response data for the created customer.
        """
        try:
            self.logger.info("Starting create_customer")

            new_customer = await self.customer_repository.create(
                name=dto.name, email=dto.email
            )
            self.customer_repository.commit()

            response_data = CustomerResponseDTO.model_validate(
                {
                    "customer_key": new_customer.customer_key,
                    "name": new_customer.name,
                    "email": new_customer.email,
                    "status": new_customer.status.enumerator,
                    "created_at": new_customer.created_at,
                    "updated_at": new_customer.updated_at,
                }
            )

            self.logger.info("create_customer completed successfully")

            return response_data

        except Exception as e:
            self.logger.error("An error occurred in create_customer", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def get_customer(self, customer_key: str) -> CustomerResponseDTO:
        """
        Retrieve a customer by its unique key.

        Args:
            customer_key (str): The unique key representing the customer.

        Returns:
            CustomerResponseDTO: The response data for the retrieved customer, or None if not found.
        """
        try:
            self.logger.info(f"Starting get_customer with customer_key: {customer_key}")

            customer = await self.customer_repository.get_by_key(customer_key)
            if not customer:
                self.logger.warning(f"Customer not found for key: {customer_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )

            response_data = CustomerResponseDTO.model_validate(
                {
                    "customer_key": customer.customer_key,
                    "name": customer.name,
                    "email": customer.email,
                    "status": customer.status.enumerator,
                    "created_at": customer.created_at,
                    "updated_at": customer.updated_at,
                }
            )

            self.logger.info(f"get_customer successfully retrieved customer_key: {customer_key}")

            return response_data

        except Exception as e:
            self.logger.error("An error occurred in get_customer", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )

    async def update_customer(
        self, customer_key: str, dto: CustomerDTO
    ) -> CustomerResponseDTO:
        """
        Update an existing customer by its unique key.

        Args:
            customer_key (str): The unique key representing the customer.
            dto (CustomerDTO): Data transfer object containing the updated customer details.

        Returns:
            CustomerResponseDTO: The response data for the updated customer, or None if not found.
        """
        try:
            self.logger.info(f"Starting update_customer with customer_key: {customer_key}")

            customer = await self.customer_repository.get_by_key(customer_key)
            if not customer:
                self.logger.warning(f"Customer not found for key: {customer_key}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )

            updated_customer = await self.customer_repository.update(
                customer, dto.name, dto.email, dto.status
            )

            self.customer_repository.commit()

            response_data = CustomerResponseDTO.model_validate(
                {
                    "customer_key": updated_customer.customer_key,
                    "name": updated_customer.name,
                    "email": updated_customer.email,
                    "status": updated_customer.status.enumerator,
                    "created_at": updated_customer.created_at,
                    "updated_at": updated_customer.updated_at,
                }
            )

            self.logger.info(f"update_customer successfully updated customer_key: {customer_key}")

            return response_data

        except Exception as e:
            self.logger.error("An error occurred in update_customer", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred"
            )
