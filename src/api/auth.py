"""
This module provides API key authentication for FastAPI routes.

Functions:
    - get_api_key: Verifies the provided API key against the configured value.
"""

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from core.config import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key"
        )
