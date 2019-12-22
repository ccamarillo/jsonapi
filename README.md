# Lite API
This is a RESTful JSON API following the JSON:API specification.  It is built with Python, Flask, and Flask-REST-JSONAPI.

https://www.palletsprojects.com/p/flask/
https://flask-rest-jsonapi.readthedocs.io/en/latest/
https://developers.google.com/classroom/guides/batch (Inspired the `POST /batch` endpoint)

At the root of the project is an Insomnia (HTTP client) JSON file.  You can import that file into Insomnia and use to hit all the endpoints.  Here's a link to download the client: https://insomnia.rest/download/#mac.  You may need to configure the base_uri environment variable in Insomnia to match your base URL.

The API exposes a `POST /batch` endpoint to handle multiple requests.  See the Insomnia file for details on how to use.

## Installation
The installation instructions assumes you have `pip` installed.
1. `pip install -r requirements.txt`
1. `flask run`  This will give you a URL.  This is the base URL that you'll need to make calls to the API

## Run Tests
1. `pytest`

## Generating a Coverage Report
1. `pytest --cov=. --cov-report term-missing`