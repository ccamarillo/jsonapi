from .. import app, db
from ..models import User
from ..libs import batch
from .support.assertions import assert_valid_schema
from .support.client import get_test_client

import json
import pytest


@pytest.fixture
def client(mocker):
    class MockRequest:
        def __init__(self, method, url):
            self.method = method
            self.url = url

    class MockResponse:
        def __init__(self, method, url, data, status_code, reason):
            self.json_data = data
            self.status_code = status_code
            self.request = MockRequest(method, url)
            self.url = url
            self.reason = reason
            self._content = json.dumps(data)

    mocker.patch(
        "app.libs.batch.Batch.run_requests",
        return_value=[
            MockResponse(
                "GET", "/users/1", {"data": "I am a user resource object."}, 200, "OK"
            ),
            MockResponse(
                "POST",
                "/users",
                {"data": "I am very sad to be a 500 error."},
                500,
                "INTERNAL SERVER ERROR",
            ),
        ],
    )
    return get_test_client()


def test_post(client):
    response = client.post("/batch", json=get_valid_request())
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert len(json_data["responses"]) == 2
    assert json_data["responses"][0]["content"] == {
        "data": "I am a user resource object."
    }
    assert json_data["responses"][0]["url"] == "/users/1"
    assert json_data["responses"][0]["method"] == "GET"
    assert json_data["responses"][0]["reason"] == "OK"
    assert json_data["responses"][1]["content"] == {
        "data": "I am very sad to be a 500 error."
    }
    assert json_data["responses"][1]["url"] == "/users"
    assert json_data["responses"][1]["method"] == "POST"
    assert json_data["responses"][1]["reason"] == "INTERNAL SERVER ERROR"


def test_post_bad_url(client):
    json_body = get_valid_request()
    json_body["data"]["requests"][0]["url"] = "not a valid url"
    response = client.post("/batch", json=json_body)
    assert response.status_code == 422
    response_body = json.loads(response.data)
    assert (
        response_body["errors"][0]["detail"]
        == 'URL must be a relative URL starting with a "/".'
    )
    assert response_body["errors"][0]["source"]["pointer"] == "/data/requests/0/url"


def test_malformed_request(client):
    json_body = {"data": {"request2": []}}
    response = client.post("/batch", json=json_body)
    assert response.status_code == 422


def get_valid_request():
    return {
        "data": {
            "requests": [
                {"method": "GET", "url": "/users/1"},
                {
                    "method": "POST",
                    "url": "/users",
                    "data": {
                        "type": "user",
                        "attributes": {
                            "email": "test@test.com",
                            "name_first": "Testy",
                            "name_last": "McTesterson",
                            "zip": "97203",
                        },
                    },
                },
            ]
        }
    }
