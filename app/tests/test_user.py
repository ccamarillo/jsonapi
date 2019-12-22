from .. import app, db
from ..models import User
from .support.assertions import assert_valid_schema
from .support.client import get_test_client

import json
import pytest


@pytest.fixture
def client():
    return get_test_client()


def test_list(client):
    response = client.get("/users")
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert_valid_schema(json_data["data"][0], "user.json")
    assert len(json_data["data"]) == 1


def test_detail(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert_valid_schema(json_data["data"], "user.json")


def test_create(client):
    response = client.post(
        "/users",
        json={
            "data": {
                "type": "user",
                "attributes": {
                    "email": "testagain@again.com",
                    "name_first": "Again",
                    "name_last": "Testing",
                    "zip": "97123",
                },
            }
        },
    )
    assert response.status_code == 201
    json_data = json.loads(response.data)
    assert_valid_schema(json_data["data"], "user.json")

    response = client.get("/users")
    json_data = json.loads(response.data)
    assert len(json_data["data"]) == 2


def test_delete(client):
    response = client.delete("/users/1")
    assert response.status_code == 200

    response = client.get("/users")
    json_data = json.loads(response.data)
    assert len(json_data["data"]) == 0


def test_patch(client):
    response = client.patch(
        "/users/1",
        json={
            "data": {
                "id": "1",
                "type": "user",
                "attributes": {
                    "email": "testagain@again.com",
                    "name_first": "Again",
                    "name_last": "Testing",
                    "zip": "97123",
                },
            }
        },
    )

    response = client.get("/users/1")
    json_data = json.loads(response.data)
    assert json_data["data"]["attributes"]["email"] == "testagain@again.com"
    assert json_data["data"]["attributes"]["name_first"] == "Again"
    assert json_data["data"]["attributes"]["name_last"] == "Testing"
    assert json_data["data"]["attributes"]["zip"] == "97123"


def test_detail_not_found(client):
    response = client.get("/users/9999999")
    assert response.status_code == 404
    json_data = json.loads(response.data)
    assert json_data["errors"][0]["source"] == "User: 9999999 not found"
