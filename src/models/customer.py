"""
This module defines the Customer model for managing customer data in the task flow system.

Classes:
    - Customer: A SQLAlchemy model that represents a customer, including attributes for customer key, status, name, email, and timestamps.
"""

from datetime import UTC, datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.customer_status import CustomerStatus

class Customer(Base):
    """
    SQLAlchemy model for representing a customer in the task flow system.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        __table_args__ (dict): Additional table options, such as schema.
        id (Column): The primary key of the customer.
        customer_key (Column): A unique key representing the customer.
        status_id (Column): A foreign key referring to the status of the customer.
        name (Column): The name of the customer.
        email (Column): The email address of the customer.
        created_at (Column): The timestamp when the customer was created.
        updated_at (Column): The timestamp when the customer was last updated.
        projects (relationship): A relationship to the projects associated with the customer.
        status (relationship): A relationship to the customer status.
    """

    __tablename__ = "Customer"
    __table_args__ = {"schema": "task_flow"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_key = Column(String(36), unique=True, nullable=False)
    status_id = Column(Integer, ForeignKey(CustomerStatus.id), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    projects = relationship("Project", back_populates="customer")

    status = relationship(
        "CustomerStatus",
        foreign_keys=[status_id],
        lazy="joined",
    )
