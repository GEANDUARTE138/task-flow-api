"""
This module contains the CustomerRepository class for managing CRUD operations 
on the Customer model.

Classes:
    - CustomerRepository: Handles the creation, retrieval, and update of customers.
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from models.customer import Customer
from models.customer_status import CustomerStatus
from repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    """
    Repository class for managing Customer model CRUD operations.

    This class provides methods for creating a new customer, retrieving a customer by key,
    and updating a customer.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the CustomerRepository with a database session.

        Args:
            session (Session): The SQLAlchemy session used to interact with the database.
        """
        super().__init__(session=session, class_name=__name__)

    async def create(self, name: str, email: str) -> Customer:
        """
        Create a new customer in the database.

        Args:
            name (str): The name of the customer.
            email (str): The email of the customer.

        Returns:
            Customer: The newly created Customer object.
        """
        new_customer = Customer()
        new_customer.customer_key = str(uuid.uuid4())
        new_customer.status = await self.get_enumerator(CustomerStatus, "active")
        new_customer.name = name
        new_customer.email = email

        self.add(new_customer)
        return new_customer

    async def get_by_key(self, customer_key: str):
        """
        Retrieve a customer from the database by their unique key.

        Args:
            customer_key (str): The unique key identifying the customer.

        Returns:
            Customer: The Customer object if found, otherwise None.
        """
        customer = self.query(Customer).filter_by(customer_key=customer_key).first()

        return customer

    async def update(
        self,
        customer: Customer,
        name: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Customer:
        """
        Update an existing customer with new information.

        Args:
            customer (Customer): The customer to be updated.
            name (Optional[str]): The new name for the customer (if provided).
            email (Optional[str]): The new email for the customer (if provided).
            status (Optional[str]): The new status for the customer (if provided).

        Returns:
            Customer: The updated Customer object.
        """
        if name:
            customer.name = name
        if email:
            customer.email = email
        if status:
            new_status = await self.get_enumerator(CustomerStatus, status)
            if new_status:
                customer.status = new_status

        return customer
