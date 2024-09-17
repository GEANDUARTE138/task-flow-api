"""
This module defines the Settings class, which holds the configuration settings for the application.

The settings include:
    - Database connection details
    - CORS origins
    - API key and headers
    - Project metadata
"""

import secrets
from typing import List, Union
from pydantic import AnyHttpUrl, ConfigDict, field_validator
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """
    Settings class that holds the configuration values for the application.

    Attributes:
        SERVICE_NAME (str): The name of the service.
        API_V1_STR (str): The versioned API prefix.
        API_KEY (str): A randomly generated API key for authentication.
        API_KEY_HEADER_NAME (str): The header name for the API key.
        DB_USER (str): The database username.
        DB_PASSWORD (str): The database password.
        DB_HOST (str): The database host address.
        DB_PORT (int): The database port.
        DB_NAME (str): The database name.
        DB_POOL_SIZE (int): The size of the database connection pool.
        DB_MAX_OVERFLOW_SIZE (int): The maximum overflow size of the connection pool.
        DB_POOL_RECYCLE_TIME (int): The time to recycle database connections in seconds.
        BACKEND_CORS_ORIGINS (List[AnyHttpUrl]): The list of allowed CORS origins.
    """
    
    SERVICE_NAME: str = "TASK FLOW API"
    API_V1_STR: str = "/v1"
    API_KEY: str = secrets.token_urlsafe(32)
    API_KEY_HEADER_NAME: str = "api-key"

    DB_USER: str = 'my_user'
    DB_PASSWORD: str = '92673269Gean.'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 3306
    DB_NAME: str = 'task_flow'
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW_SIZE: int = 10
    DB_POOL_RECYCLE_TIME: int = 900

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validate and assembles the CORS origins.

        Args:
            v (Union[str, List[str]]): A string or list of CORS origin URLs.

        Returns:
            Union[List[str], str]: A list of CORS origin URLs.

        Raises:
            ValueError: If the input value is not a valid string or list of strings.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
