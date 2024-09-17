"""
This module defines the BaseService class, which provides a base service with logging functionality.

Classes:
    - BaseService: An abstract base class that provides logging for derived services.
"""

from abc import ABCMeta
from utils.logger import Logger


class BaseService(metaclass=ABCMeta):
    """
    Abstract base service class that provides logging functionality.

    Attributes:
        logger (Logger): An instance of the Logger class for logging messages.
    """

    def __init__(self, class_name: str) -> None:
        """
        Initialize the BaseService with a logger.

        Args:
            class_name (str): The name of the class using the service, used for logging.
        """
        self.logger = Logger(class_name)
