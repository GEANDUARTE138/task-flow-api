"""
This module sets up the FastAPI application, including CORS middleware, 
database connection management, and API routing.

It defines functions for initializing the application, managing resources during startup
and shutdown, and handling HTTP request middleware.

Functions:
    - on_startup: Initialize resources when the application starts.
    - on_shutdown: Clean up resources when the application shuts down.
    - create: Create and configure the FastAPI app instance.
    - main: Entry point for initializing logging and environment variable checks.
    - handle_input_output: Middleware for processing HTTP requests and responses.
"""

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from api.api import router
from connector.mysql_connector import MySQLConnector
from core.config import settings
from shared.constants import PROJECT_DESCRIPTION, SERVICE_NAME, check_variables
from utils.logger import LogHandler


async def on_startup():
    """
    Initialize resources at application startup.

    This function sets up the MySQL database engine and logs a startup message.
    """
    MySQLConnector.create_engine()
    print(f"Service {SERVICE_NAME} starting...")


async def on_shutdown():
    """
    Clean up resources at application shutdown.

    This function disposes of the MySQL database engine and logs a shutdown message.
    """
    MySQLConnector.dispose_engine()
    print(f"Service {SERVICE_NAME} shutting down...")


def create() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function sets up the FastAPI app with title, description, version, and OpenAPI URL.
    It also configures CORS middleware and includes the API router.
    
    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    api = FastAPI(
        title=settings.SERVICE_NAME,
        description=PROJECT_DESCRIPTION,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )

    if settings.BACKEND_CORS_ORIGINS:
        api.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    api.include_router(router, prefix=settings.API_V1_STR)

    return api


def main():
    """
    Entry point for initializing logging, checking environment variables, and creating the app.

    This function checks required environment variables, initializes logging, and 
    creates the FastAPI app instance.
    
    Returns:
        FastAPI: The FastAPI application instance.
    """
    check_variables()
    LogHandler()
    app = create()
    return app


app = main()


@app.middleware("http")
async def handle_input_output(request: Request, call_next):
    """
    Middleware for handling input and output of HTTP requests.

    This middleware processes HTTP requests and skips specific paths such as `/docs` and `/favicon.ico`.
    It passes the request to the next handler and returns the response.

    Args:
        request (Request): The incoming HTTP request.
        call_next: The next middleware or route handler.

    Returns:
        Response: The HTTP response after processing.
    """
    if request.url.path in [
        "/favicon.ico",
        "/docs",
        "/v1/openapi.json",
        "/redoc",
    ]:
        return await call_next(request)

    response = await call_next(request)

    return response
