from unittest.mock import AsyncMock, MagicMock

import pytest

from schemas.activity import ActivityDTO, ActivityResponseDTO, ActivityUpdateDTO
from services.activity import ActivityService


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
