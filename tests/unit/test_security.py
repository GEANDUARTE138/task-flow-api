from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import pytest
from unittest.mock import patch
from api.auth import get_api_key  # Supondo que get_api_key está no módulo api_key_auth
from core.config import settings

@pytest.mark.asyncio
async def test_get_api_key_valid():
    # Simular a API Key correta
    with patch("core.config.settings.API_KEY", "valid-api-key"):
        # Chamar a função passando a chave correta
        result = await get_api_key("valid-api-key")
        assert result == "valid-api-key"

@pytest.mark.asyncio
async def test_get_api_key_invalid():
    # Simular a API Key correta, mas passar uma chave incorreta
    with patch("core.config.settings.API_KEY", "valid-api-key"):
        with pytest.raises(HTTPException) as excinfo:
            await get_api_key("invalid-api-key")

        # Verificar se a exceção HTTP 401 é levantada
        assert excinfo.value.status_code == HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Invalid or missing API Key"

@pytest.mark.asyncio
async def test_get_api_key_missing():
    # Simular a ausência da API Key no cabeçalho
    with patch("core.config.settings.API_KEY", "valid-api-key"):
        with pytest.raises(HTTPException) as excinfo:
            await get_api_key(None)  # Nenhuma chave fornecida

        # Verificar se a exceção HTTP 401 é levantada
        assert excinfo.value.status_code == HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Invalid or missing API Key"
