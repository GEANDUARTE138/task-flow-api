from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from schemas.project import ProjectDTO, ProjectResponseDTO, ProjectUpdateDTO
from services.project import ProjectService


@pytest.mark.asyncio
async def test_create_project(db_session):
    session = MagicMock()
    project_repository = AsyncMock()
    customer_repository = AsyncMock()

    customer_mock = MagicMock()
    customer_mock.customer_key = "customer-key"
    customer_repository.get_by_key.return_value = customer_mock

    project_mock = MagicMock()
    project_mock.project_key = "project-key"
    project_mock.name = "Project Name"
    project_mock.status.enumerator = (
        "open"  
    )
    project_mock.due_date = datetime(2024, 2, 1, 0, 0, 0) 
    project_mock.created_at = datetime(2024, 1, 1, 0, 0, 0)
    project_mock.updated_at = datetime(2024, 1, 1, 0, 0, 0)
    project_repository.create.return_value = project_mock

    service = ProjectService(session)
    service.project_repository = project_repository
    service.customer_repository = customer_repository

    dto = ProjectDTO(
        name="Project Name",
        customer_key="customer-key",
        due_date=datetime(2024, 2, 1, 0, 0, 0),
    )

    result = await service.create_project(dto)

    assert db_session is not None
    assert isinstance(result, ProjectResponseDTO)
    assert result.name == "Project Name"
    assert result.status == "open"
    assert result.project_key == "project-key"
    assert result.due_date == datetime(2024, 2, 1, 0, 0, 0)

    project_repository.create.assert_called_once_with(
        "Project Name", customer_mock, datetime(2024, 2, 1, 0, 0, 0)
    )
    customer_repository.get_by_key.assert_called_once_with("customer-key")


@pytest.mark.asyncio
async def test_get_project(db_session):
    session = MagicMock()
    project_repository = AsyncMock()

    project_mock = MagicMock()
    project_mock.project_key = "project-key"
    project_mock.name = "Existing Project"
    project_mock.status.enumerator = "open"
    project_mock.customer.customer_key = "customer-key"
    project_mock.created_at = datetime(2024, 1, 1, 0, 0, 0)
    project_mock.updated_at = datetime(2024, 1, 1, 0, 0, 0)

    project_repository.get_by_key.return_value = project_mock

    service = ProjectService(session)
    service.project_repository = project_repository

    result = await service.get_project("project-key")

    assert db_session is not None
    assert isinstance(result, ProjectResponseDTO)
    assert result.project_key == "project-key"
    assert result.name == "Existing Project"
    assert result.status == "open"
    assert result.customer_key == "customer-key"
    assert result.created_at == datetime(2024, 1, 1, 0, 0, 0)
    assert result.updated_at == datetime(2024, 1, 1, 0, 0, 0)

    project_repository.get_by_key.assert_called_once_with("project-key")


@pytest.mark.asyncio
async def test_update_project(db_session):
    session = MagicMock()
    project_repository = AsyncMock()

    project_mock = MagicMock()
    project_mock.project_key = "project-key"
    project_mock.name = "Existing Project"
    project_mock.status.enumerator = "open"
    project_mock.customer.customer_key = "customer-key"
    project_mock.created_at = datetime(2024, 1, 1, 0, 0, 0)
    project_mock.updated_at = datetime(2024, 1, 1, 0, 0, 0)

    project_repository.get_by_key.return_value = project_mock

    updated_project_mock = MagicMock()
    updated_project_mock.project_key = "project-key"
    updated_project_mock.name = "Updated Project"
    updated_project_mock.status.enumerator = "closed"
    updated_project_mock.customer.customer_key = "customer-key"
    updated_project_mock.created_at = datetime(2024, 1, 1, 0, 0, 0)
    updated_project_mock.updated_at = datetime(2024, 1, 2, 0, 0, 0)

    project_repository.update.return_value = updated_project_mock

    service = ProjectService(session)
    service.project_repository = project_repository

    dto = ProjectUpdateDTO(name="Updated Project", status="closed")

    result = await service.update_project("project-key", dto)

    assert db_session is not None
    assert isinstance(result, ProjectResponseDTO)
    assert result.name == "Updated Project"
    assert result.status == "closed"
    assert result.customer_key == "customer-key"
    assert result.updated_at == datetime(2024, 1, 2, 0, 0, 0)

    project_repository.get_by_key.assert_called_once_with("project-key")
    project_repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_list_projects_with_due_date_and_status(db_session):
    session = MagicMock()
    project_repository = AsyncMock()
    customer_repository = AsyncMock()

    customer_mock = MagicMock()
    customer_mock.customer_key = "customer-key"
    customer_repository.get_by_key.return_value = customer_mock

    project_repository.count_projects_by_customer.return_value = 10

    project_mock = MagicMock()
    project_mock.project_key = "project-key"
    project_mock.name = "Filtered Project"
    project_mock.status.enumerator = "open"
    project_mock.created_at = datetime(2024, 1, 1, 0, 0, 0)
    project_mock.updated_at = datetime(2024, 1, 1, 0, 0, 0)
    project_mock.due_date = datetime(2024, 2, 1, 0, 0, 0)
    project_repository.list_projects_by_customer.return_value = [project_mock]

    service = ProjectService(session)
    service.project_repository = project_repository
    service.customer_repository = customer_repository

    result = await service.list_projects_by_customer(
        customer_key="customer-key",
        include_activities=False,
        status="open",
        due_date="2024-02-01",
        limit=10,
        page=1,
    )

    assert result.total_items == 10
    assert len(result.projects) == 1
    assert result.projects[0].name == "Filtered Project"
    assert result.projects[0].status == "open"
    assert result.projects[0].due_date == datetime(2024, 2, 1, 0, 0, 0)

    project_repository.count_projects_by_customer.assert_called_once_with(
        customer_mock.id, "open", "2024-02-01"
    )
    project_repository.list_projects_by_customer.assert_called_once_with(
        customer_mock.id, "open", "2024-02-01", 10, 1
    )
