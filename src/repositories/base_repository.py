"""
This module contains the BaseRepository class, which provides common database
operations for other repositories.

The BaseRepository offers methods for adding, querying, and managing models
in the database, as well as handling transactions such as commit and rollback.

Classes:
    - BaseRepository: An abstract base class that provides common database CRUD operations.
"""

from abc import ABCMeta
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from utils.logger import Logger


class BaseRepository(metaclass=ABCMeta):
    """
    Abstract base repository class for managing common database operations.

    This class provides methods for committing, querying, adding, and managing models 
    in the database.
    """

    def __init__(self, class_name: str, session: Session) -> None:
        """
        Initialize the BaseRepository with a database session and logger.

        Args:
            class_name (str): The name of the class using this repository (used for logging).
            session (Session): The SQLAlchemy session used to interact with the database.
        """
        self.__session = session
        self.logger = Logger(class_name)

    def flush(self) -> None:
        """
        Flush the current session.

        This method sends any pending changes to the database without committing the transaction.
        """
        self.__session.flush()

    def refresh(self, model) -> None:
        """
        Refresh the state of a model from the database.

        Args:
            model: The model to be refreshed.
        """
        self.__session.refresh(model)

    def expire(self, model) -> None:
        """
        Mark the model instance as expired.

        Args:
            model: The model instance to be expired.
        """
        self.__session.expire(model)

    def get_all(self, model_class):
        """
        Retrieve all instances of a model class from the database.

        Args:
            model_class: The model class to retrieve.

        Returns:
            List: A list of all model instances.
        """
        return self.__session.query(model_class).all()

    def commit(self) -> None:
        """
        Commit the current transaction.

        This method applies all changes made in the current session to the database.
        """
        self.__session.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.

        This method reverts any changes made in the current session.
        """
        self.__session.rollback()

    def add(self, model) -> None:
        """
        Add a new model instance to the session.

        Args:
            model: The model instance to be added.
        """
        self.__session.add(model)

    def query(self, *models) -> Query:
        """
        Query the database for one or more models.

        Args:
            models: The models to query for.

        Returns:
            Query: A SQLAlchemy Query object for the models.
        """
        return self.__session.query(*models)

    async def get_enumerator(self, model, enumerator):
        """
        Retrieve a single enumerator from the model based on a value.

        Args:
            model: The model to query.
            enumerator: The value to filter the enumerator by.

        Returns:
            The enumerator matching the specified value.
        """
        return self.__session.query(model).filter(model.enumerator == enumerator).one()

    async def get_enumerators(self, model, enumerators: list):
        """
        Retrieve multiple enumerators from the model based on a list of values.

        Args:
            model: The model to query.
            enumerators (list): A list of enumerator values to filter by.

        Returns:
            List: A list of enumerators matching the specified values.
        """
        return (
            self.__session.query(model).filter(model.enumerator.in_(enumerators)).all()
        )
