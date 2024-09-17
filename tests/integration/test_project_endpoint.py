import os
import time

import pytest
from dotenv import load_dotenv
from faker import Faker
from fastapi.testclient import TestClient

load_dotenv()

faker = Faker()


@pytest.mark.asyncio
async def test_create_project(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data = {"name": faker.company(), "customer_key": customer_key}

    project_response = client.post("/v1/project", json=project_data, headers=headers)
    assert project_response.status_code == 200, f"Erro: {project_response.text}"

    project_data_response = project_response.json()
    assert project_data_response["name"] == project_data["name"]
    assert project_data_response["customer_key"] == customer_key


@pytest.mark.asyncio
async def test_get_project(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data = {"name": faker.company(), "customer_key": customer_key}

    project_response = client.post("/v1/project", json=project_data, headers=headers)
    assert project_response.status_code == 200, f"Erro: {project_response.text}"
    project_key = project_response.json()["project_key"]

    get_response = client.get(f"/v1/project/{project_key}", headers=headers)
    assert get_response.status_code == 200, f"Erro: {get_response.text}"
    project_data_response = get_response.json()

    assert project_data_response["project_key"] == project_key
    assert project_data_response["name"] == project_data["name"]
    assert project_data_response["customer_key"] == customer_key


@pytest.mark.asyncio
async def test_update_project(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data = {"name": faker.company(), "customer_key": customer_key}

    project_response = client.post("/v1/project", json=project_data, headers=headers)
    assert project_response.status_code == 200, f"Erro: {project_response.text}"
    project_key = project_response.json()["project_key"]

    update_data = {
        "name": faker.company(),  
        "status": "closed",  
    }

    update_response = client.put(
        f"/v1/project/{project_key}", json=update_data, headers=headers
    )
    assert update_response.status_code == 200, f"Erro: {update_response.text}"
    updated_project_data = update_response.json()

    assert updated_project_data["project_key"] == project_key
    assert updated_project_data["name"] == update_data["name"]
    assert updated_project_data["status"] == update_data["status"]
    assert updated_project_data["customer_key"] == customer_key


@pytest.mark.asyncio
async def test_list_projects_with_filters(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert (
        customer_response.status_code == 200
    ), f"Erro ao criar cliente: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data_1 = {
        "name": faker.company(),
        "customer_key": customer_key,
        "due_date": "2024-02-01",
    }

    project_data_2 = {
        "name": faker.company(),
        "customer_key": customer_key,
        "due_date": "2024-02-02",
        "status": "closed",
    }

    project_response_1 = client.post(
        "/v1/project", json=project_data_1, headers=headers
    )
    project_response_2 = client.post(
        "/v1/project", json=project_data_2, headers=headers
    )

    assert (
        project_response_1.status_code == 200
    ), f"Erro ao criar o primeiro projeto: {project_response_1.text}"
    assert (
        project_response_2.status_code == 200
    ), f"Erro ao criar o segundo projeto: {project_response_2.text}"

    project_key_1 = project_response_1.json()["project_key"]
    project_key_2 = project_response_2.json()["project_key"]

    list_response_no_filters = client.get(
        f"/v1/projects/{customer_key}", headers=headers
    )
    assert (
        list_response_no_filters.status_code == 200
    ), f"Erro ao listar projetos sem filtros: {list_response_no_filters.text}"

    projects_no_filters = list_response_no_filters.json()
    assert (
        len(projects_no_filters["projects"]) > 0
    ), "Nenhum projeto foi encontrado sem filtro."
    print("Projetos retornados sem filtro:", projects_no_filters)

    params = {"status": "open", "due_date": "2024-02-01", "page": 1, "limit": 10}

    list_response = client.get(
        f"/v1/projects/{customer_key}", headers=headers, params=params
    )
    assert (
        list_response.status_code == 200
    ), f"Erro ao listar projetos com filtros: {list_response.text}"

    projects_data = list_response.json()

    print("Projetos retornados com filtro:", projects_data)
    assert (
        projects_data["total_items"] > 0
    ), "Nenhum projeto foi retornado, esperado pelo menos 1."

    assert any(
        project["project_key"] == project_key_1 for project in projects_data["projects"]
    ), "Projeto com due_date '2024-02-01' não encontrado."

    assert not any(
        project["project_key"] == project_key_2 for project in projects_data["projects"]
    ), "Projeto com status 'closed' foi encontrado, mas deveria estar filtrado."
