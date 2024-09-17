from unittest.mock import AsyncMock, MagicMock

import pytest

from schemas.activity import ActivityDTO, ActivityResponseDTO, ActivityUpdateDTO
from services.activity import ActivityService
from fastapi import HTTPException
from datetime import datetime

@pytest.mark.asyncio
async def test_create_activity(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()
    project_repository = AsyncMock()

    project_repository.get_by_key.return_value = MagicMock(project_key="project-key")

    activity_repository.create.return_value = MagicMock(
        activity_key="activity-key",
        description="New Activity",
        status=MagicMock(enumerator="not_started"),
        due_date=None,
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )

    service = ActivityService(session)
    service.activity_repository = activity_repository
    service.project_repository = project_repository

    dto = ActivityDTO(
        description="New Activity",
        due_date=None,
        project_key="project-key", 
    )

    result = await service.create_activity(dto)

    assert db_session is not None
    assert isinstance(result, ActivityResponseDTO)
    assert result.activity_key == "activity-key"
    assert result.description == "New Activity"
    assert result.status == "not_started"

    activity_repository.create.assert_called_once_with(
        "New Activity", None, project_repository.get_by_key.return_value
    )
    project_repository.get_by_key.assert_called_once_with("project-key")


@pytest.mark.asyncio
async def test_create_activity_project_not_found(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()
    project_repository = AsyncMock()

    # Simular que o projeto não foi encontrado
    project_repository.get_by_key.return_value = None

    service = ActivityService(session)
    service.activity_repository = activity_repository
    service.project_repository = project_repository

    dto = ActivityDTO(
        description="New Activity",
        due_date=None,
        project_key="invalid-project-key",
    )

    # Verifique se uma exceção HTTP 404 é levantada
    with pytest.raises(HTTPException) as excinfo:
        await service.create_activity(dto)
    
    # Garantir que o código de status retornado seja 404
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Project not found"
    project_repository.get_by_key.assert_called_once_with("invalid-project-key")
    activity_repository.create.assert_not_called()


@pytest.mark.asyncio
async def test_get_activity(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()

    activity_repository.get_by_key.return_value = MagicMock(
        activity_key="activity-key",
        description="Existing Activity",
        status=MagicMock(enumerator="not_started"),
        project=MagicMock(project_key="project-key"),
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )

    service = ActivityService(session)
    service.activity_repository = activity_repository

    result = await service.get_activity("activity-key")

    assert db_session is not None
    assert isinstance(result, ActivityResponseDTO)
    assert result.activity_key == "activity-key"
    assert result.description == "Existing Activity"
    assert result.status == "not_started"
    activity_repository.get_by_key.assert_called_once_with("activity-key")


@pytest.mark.asyncio
async def test_update_activity(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()

    activity_repository.get_by_key.return_value = MagicMock(
        activity_key="activity-key",
        description="Existing Activity",
        status=MagicMock(enumerator="not_started"),
        project=MagicMock(project_key="project-key"),
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )

    activity_repository.update.return_value = MagicMock(
        activity_key="activity-key",
        description="Updated Activity",
        status=MagicMock(enumerator="in_progress"),
        project=MagicMock(project_key="project-key"),
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-02T00:00:00",
    )

    service = ActivityService(session)
    service.activity_repository = activity_repository

    dto = ActivityUpdateDTO(description="Updated Activity", status="in_progress")

    result = await service.update_activity("activity-key", dto)

    assert db_session is not None
    assert isinstance(result, ActivityResponseDTO)
    assert result.description == "Updated Activity"
    assert result.status == "in_progress"
    activity_repository.get_by_key.assert_called_once_with("activity-key")
    activity_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_get_activity_not_found(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()

    # Simular que a atividade não foi encontrada
    activity_repository.get_by_key.return_value = None

    service = ActivityService(session)
    service.activity_repository = activity_repository

    # Verifique se uma exceção HTTP 404 é levantada
    with pytest.raises(HTTPException) as excinfo:
        await service.get_activity("nonexistent-activity-key")

    # Garantir que o código de status retornado seja 404
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Activity not found"
    activity_repository.get_by_key.assert_called_once_with("nonexistent-activity-key")



@pytest.mark.asyncio
async def test_create_activity_internal_error(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()
    project_repository = AsyncMock()

    # Simular que o projeto é encontrado
    project_repository.get_by_key.return_value = MagicMock(project_key="project-key")

    # Simular um erro ao criar uma atividade
    activity_repository.create.side_effect = Exception("Database error")

    service = ActivityService(session)
    service.activity_repository = activity_repository
    service.project_repository = project_repository

    dto = ActivityDTO(
        description="New Activity",
        due_date=None,
        project_key="project-key",
    )

    with pytest.raises(HTTPException) as excinfo:
        await service.create_activity(dto)

    assert excinfo.value.status_code == 500
    assert "internal error" in str(excinfo.value.detail).lower()
    project_repository.get_by_key.assert_called_once_with("project-key")
    activity_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_activity_internal_error(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()

    # Simular um erro ao tentar recuperar a atividade
    activity_repository.get_by_key.side_effect = Exception("Database error")

    service = ActivityService(session)
    service.activity_repository = activity_repository

    with pytest.raises(HTTPException) as excinfo:
        await service.get_activity("activity-key")

    assert excinfo.value.status_code == 500
    assert "internal error" in str(excinfo.value.detail).lower()
    activity_repository.get_by_key.assert_called_once_with("activity-key")


@pytest.mark.asyncio
async def test_update_activity_internal_error(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()

    # Simular que a atividade foi encontrada
    activity_repository.get_by_key.return_value = MagicMock(
        activity_key="activity-key",
        description="Existing Activity",
        status=MagicMock(enumerator="not_started"),
        project=MagicMock(project_key="project-key"),
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )

    # Simular um erro ao tentar atualizar a atividade
    activity_repository.update.side_effect = Exception("Database error")

    service = ActivityService(session)
    service.activity_repository = activity_repository

    dto = ActivityUpdateDTO(description="Updated Activity", status="in_progress")

    with pytest.raises(HTTPException) as excinfo:
        await service.update_activity("activity-key", dto)

    assert excinfo.value.status_code == 500
    assert "internal error" in str(excinfo.value.detail).lower()
    activity_repository.get_by_key.assert_called_once_with("activity-key")
    activity_repository.update.assert_called_once()



@pytest.mark.asyncio
async def test_create_activity_with_due_date(db_session):
    session = MagicMock()
    activity_repository = AsyncMock()
    project_repository = AsyncMock()

    project_repository.get_by_key.return_value = MagicMock(project_key="project-key")

    # Aqui, a data será passada como um objeto datetime, não como string
    activity_repository.create.return_value = MagicMock(
        activity_key="activity-key",
        description="New Activity",
        status=MagicMock(enumerator="not_started"),
        due_date=datetime(2024, 2, 1),
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        updated_at=datetime(2024, 1, 1, 0, 0, 0),
    )

    service = ActivityService(session)
    service.activity_repository = activity_repository
    service.project_repository = project_repository

    # Passar a due_date como um objeto datetime
    dto = ActivityDTO(
        description="New Activity",
        due_date=datetime(2024, 2, 1),  # Use um objeto datetime
        project_key="project-key",
    )

    result = await service.create_activity(dto)

    assert db_session is not None
    assert isinstance(result, ActivityResponseDTO)
    assert result.activity_key == "activity-key"
    assert result.description == "New Activity"
    assert result.status == "not_started"
    
    # Comparar a data de vencimento no formato esperado
    assert result.due_date.strftime("%Y-%m-%d") == "2024-02-01"

    # Aqui o esperado é um datetime, então ajustamos o teste
    activity_repository.create.assert_called_once_with(
        "New Activity", datetime(2024, 2, 1), project_repository.get_by_key.return_value
    )
