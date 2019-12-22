from .. import app
from .exceptions import ValidationException

import grequests
from jsonschema import validate

import json
import inspect


class Batch:
    """
    Initialize and validate request
    param request
    return string
    """

    def __init__(self, request):
        validate(request.json, self.get_validate_schema())
        self.validate_urls(request.json)
        self.request = request
        self.results = [{} for x in self.request.get_json()["data"]["requests"]]
        self.threads = []

    """
    Run the requests and return the response JSON
    return string
    """

    def execute(self):
        self.requests = self.request.get_json()["data"]["requests"]
        responses = self.run_requests(self.requests)
        return self.get_response_json(responses)

    """
    Build a JSON body for response
    param responses
    return string
    """

    def get_response_json(self, responses):
        responseJson = {"responses": []}
        for response in responses:
            theResponse = {}
            theResponse["method"] = response.request.method
            theResponse["url"] = response.url
            theResponse["status_code"] = response.status_code
            reason = response.reason
            theResponse["reason"] = reason
            theResponse["content"] = json.loads(response._content)
            responseJson["responses"].append(theResponse)
        return responseJson

    """
    Get the validation schema for request
    return obj
    """

    def get_validate_schema(self):
        return {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "requests": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "method": {
                                        "type": "string",
                                        "enum": [
                                            "GET",
                                            "PATCH",
                                            "POST",
                                            "DELETE",
                                            "OPTIONS",
                                        ],
                                    },
                                    "url": {"type": "string"},
                                    "data": {
                                        "type": "object",
                                        "properties": {
                                            "type": {"type": "string"},
                                            "id": {"type": "string"},
                                            "attributes": {"type": "object"},
                                        },
                                    },
                                },
                                "required": ["method", "url"],
                            },
                        }
                    },
                    "required": ["requests"],
                }
            },
            "required": ["data"],
            "additionalProperties": False,
        }

    """
    Builds a list of requests to run a separate threads, runs the requests, and gathers the results
    This lacks test coverage because I'm getting internal errors in the test.  
    I think it has to do with the test client not having a domain.
    So I am mocking this in tests.
    param request
    return list
    """

    def run_requests(self, requests):
        rs = []
        for theRequest in requests:
            method = theRequest["method"]
            url = self.request.url_root.rstrip("/") + theRequest["url"]
            if method == "GET":
                rs.append(grequests.get(url))
            if method == "DELETE":
                rs.append(grequests.delete(url))
            if method == "OPTIONS":
                rs.append(grequests.options(url))
            if method == "POST":
                rs.append(grequests.post(url, json=theRequest))
            if method == "PATCH":
                rs.append(grequests.patch(url, json=theRequest))

        return grequests.map(rs)

    def validate_urls(self, data):
        request_index = 0
        for request in data["data"]["requests"]:
            if request["url"][0] != "/":
                raise ValidationException(
                    'URL must be a relative URL starting with a "/".',
                    f"/data/requests/{request_index}/url",
                )
            request_index = request_index + 1
