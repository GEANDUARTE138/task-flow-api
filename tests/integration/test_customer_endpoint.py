import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from fastapi.testclient import TestClient

load_dotenv()

faker = Faker()


@pytest.mark.asyncio
async def test_create_customer(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {
        "api-key": os.getenv(
            "API_KEY"
        )  
    }

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"

    customer_data_response = customer_response.json()
    assert customer_data_response["name"] == customer_data["name"]
    assert customer_data_response["email"] == customer_data["email"]


@pytest.mark.asyncio
async def test_get_customer(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    get_response = client.get(f"/v1/customer/{customer_key}", headers=headers)
    assert get_response.status_code == 200, f"Erro: {get_response.text}"
    customer_data_response = get_response.json()

    assert customer_data_response["customer_key"] == customer_key
    assert customer_data_response["name"] == customer_data["name"]
    assert customer_data_response["email"] == customer_data["email"]


@pytest.mark.asyncio
async def test_update_customer(client: TestClient):
    customer_data = {"name": faker.name(), "email": faker.email()}

    headers = {"api-key": os.getenv("API_KEY")}

    customer_response = client.post("/v1/customer", json=customer_data, headers=headers)
    assert customer_response.status_code == 200, f"Erro: {customer_response.text}"
    customer_key = customer_response.json()["customer_key"]

    update_data = {
        "name": faker.name(), 
        "email": faker.email(),
        "status": "inactive",
    }

    update_response = client.put(
        f"/v1/customer/{customer_key}", json=update_data, headers=headers
    )
    assert update_response.status_code == 200, f"Erro: {update_response.text}"
    updated_customer_data = update_response.json()

    assert updated_customer_data["customer_key"] == customer_key
    assert updated_customer_data["name"] == update_data["name"]
    assert updated_customer_data["email"] == update_data["email"]
    assert updated_customer_data["status"] == update_data["status"]
