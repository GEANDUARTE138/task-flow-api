"""
This module defines a Singleton metaclass to ensure that a class only has one instance.

Classes:
    - Singleton: A metaclass that implements the Singleton design pattern.
"""

class Singleton(type):
    """
    A Singleton metaclass that ensures only one instance of a class is created.

    The Singleton pattern restricts the instantiation of a class to a single object.
    This is useful when exactly one object is needed to coordinate actions across a system.

    Attributes:
        _instances (dict): A dictionary that stores the single instance of each class that uses this metaclass.
    """
    
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Override the __call__ method to control the instantiation of the class.

        If an instance of the class does not already exist, create and store it.
        If it exists, return the existing instance.

        Args:
            *args: Positional arguments for class instantiation.
            **kwargs: Keyword arguments for class instantiation.

        Returns:
            object: The single instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
