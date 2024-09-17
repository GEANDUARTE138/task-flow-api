import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from fastapi.testclient import TestClient

load_dotenv()

faker = Faker()


@pytest.mark.asyncio
async def test_create_activity(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data = {
        "name": faker.company(), 
        "customer_key": customer_key,
    }

    project_response = client.post("/v1/project", json=project_data, headers=headers)
    assert project_response.status_code == 200, f"Erro: {project_response.text}"
    project_key = project_response.json()["project_key"]

    activity_data = {"description": "New Activity", "project_key": project_key}

    activity_response = client.post("/v1/activity", json=activity_data, headers=headers)
    assert activity_response.status_code == 200, f"Erro: {activity_response.text}"
    activity_data_response = activity_response.json()
    assert activity_data_response["description"] == "New Activity"
    assert activity_data_response["project_key"] == project_key


@pytest.mark.asyncio
async def test_get_activity(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data = {"name": faker.company(), "customer_key": customer_key}

    project_response = client.post("/v1/project", json=project_data, headers=headers)
    assert project_response.status_code == 200, f"Erro: {project_response.text}"
    project_key = project_response.json()["project_key"]

    activity_data = {"description": "New Activity", "project_key": project_key}

    activity_response = client.post("/v1/activity", json=activity_data, headers=headers)
    assert activity_response.status_code == 200, f"Erro: {activity_response.text}"
    activity_key = activity_response.json()["activity_key"]

    get_response = client.get(f"/v1/activity/{activity_key}", headers=headers)
    assert get_response.status_code == 200, f"Erro: {get_response.text}"
    activity_data_response = get_response.json()
    assert activity_data_response["activity_key"] == activity_key
    assert activity_data_response["description"] == "New Activity"
    assert activity_data_response["project_key"] == project_key


@pytest.mark.asyncio
async def test_update_activity(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    project_data = {"name": faker.company(), "customer_key": customer_key}

    project_response = client.post("/v1/project", json=project_data, headers=headers)
    assert project_response.status_code == 200, f"Erro: {project_response.text}"
    project_key = project_response.json()["project_key"]

    activity_data = {"description": "New Activity", "project_key": project_key}

    activity_response = client.post("/v1/activity", json=activity_data, headers=headers)
    assert activity_response.status_code == 200, f"Erro: {activity_response.text}"
    activity_key = activity_response.json()["activity_key"]

    update_data = {"description": "Updated Activity", "status": "in_progress"}

    update_response = client.put(
        f"/v1/activity/{activity_key}", json=update_data, headers=headers
    )
    assert update_response.status_code == 200, f"Erro: {update_response.text}"
    updated_activity_data = update_response.json()

    assert updated_activity_data["description"] == "Updated Activity"
    assert updated_activity_data["status"] == "in_progress"
    assert updated_activity_data["activity_key"] == activity_key
