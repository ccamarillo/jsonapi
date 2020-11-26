# Lite API
This is a RESTful JSON API following the JSON:API specification.  It is built with Python, Flask, and Flask-REST-JSONAPI.

- https://www.palletsprojects.com/p/flask/
- https://flask-rest-jsonapi.readthedocs.io/en/latest/

At the root of the project is an Insomnia (HTTP client) JSON file.  You can import that file into Insomnia and use to hit all the endpoints.  Here's a link to download the client: https://insomnia.rest/download/#mac.  You may need to configure the base_uri environment variable in Insomnia to match your base URL.

It's here to illustrate my knowledge of API design in general and REST:API in particular.

There is work-in progress on a batch processing endpoint, inspired by https://developers.google.com/classroom/guides/batch.

## Run it with Docker
1. `docker-compose up --build`

## Run Tests
1. Pop into the docker container with `docker exec -it lite-api_web_1 /bin/bash`
1. `pytest`

## Generating a Coverage Report
1. Inside the Docker container, `pytest --cov=. --cov-report term-missing`
