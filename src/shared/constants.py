"""
This module contains constants and utility functions for the task-flow project.

Constants:
    - SERVICE_ROOT: The root directory of the service.
    - SCHEMA_PATH: The path to the schemas directory.
    - SERVICE_NAME: The name of the service, retrieved from environment variables.
    - PROJECT_DESCRIPTION: A description of the task-flow project.
    - APP_ENV: The application environment, retrieved from environment variables.
    - PROJECT_ENV: The project environment, retrieved from environment variables.
    - BYPASS_ENDPOINTS: A list of endpoints that bypass authentication.
    - BYPASS_ENDPOINTS_DOCS: A list of documentation-related endpoints that bypass authentication.

Functions:
    - check_variables: Checks if environment variables or constants are missing values.
"""

import os


SERVICE_ROOT = os.path.abspath(os.path.dirname(__file__))
SCHEMA_PATH = SERVICE_ROOT + "/schemas/"
SERVICE_NAME = os.environ.get("SERVICE_NAME")
PROJECT_DESCRIPTION: str = """
Este projeto visa desenvolver uma nova plataforma de gestão de projetos e desenvolvimento de software para a Microsoft, substituindo o sistema legado desktop por uma solução acessível pela internet. 
A plataforma permite o planejamento e acompanhamento de times, projetos, clientes e tarefas, facilitando o gerenciamento colaborativo de forma remota. 
A solução foi projetada para atender às necessidades modernas de acessibilidade e colaboração, possibilitando que colaboradores e clientes acessem o sistema de qualquer lugar, especialmente em um contexto de trabalho remoto.
"""


APP_ENV = os.environ.get("APP_ENV")
PROJECT_ENV = os.environ.get("PROJECT_ENV")

BYPASS_ENDPOINTS = ["/", "/health_check"]
BYPASS_ENDPOINTS_DOCS = ["/docs", "/docs/api.json", "/redoc"]


def check_variables():
    """
    Check if critical environment variables or constants are missing values.

    This function checks all global variables in the module. If any integer, float,
    or string variables are missing values (e.g., -1 or an empty string), it raises
    an EnvironmentError listing the variables that are missing values.

    Raises:
        EnvironmentError: If any required variables are missing values.
    """
    variable_names = [
        k for k in dir() if (k[:2] != "__" and not callable(globals()[k]))
    ]
    variables_without_value = []
    for variable in variable_names:
        variable_value = globals()[variable]
        if isinstance(variable_value, int) and variable_value == -1:
            variables_without_value.append(variable)
        elif isinstance(variable_value, float) and variable_value == -1:
            variables_without_value.append(variable)
        elif isinstance(variable_value, str) and not variable_value:
            variables_without_value.append(variable)
    if variables_without_value:
        raise EnvironmentError(
            "A Error occurred while checking variables, please verify these variables without values {}".format(
                variables_without_value
            )
        )
