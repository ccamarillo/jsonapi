# Lite API
This is a RESTful JSON API following the JSON:API specification.  It is built with Python, Flask, and Flask-REST-JSONAPI.

I've attached an Insomnia (http client) JSON file that you can import and use to hit all the endpoints.  Here's a link to download the client: https://insomnia.rest/download/#mac.  You may need to configure the base_uri environment variable in Insomnia to match your base URL.

## Installation
The installation instructions assumes you have `pip` installed.
1. `pip install -r requirements.txt`
1. `flask run`  This will give you a URL.  This is the base URL that you'll need to make calls to the API

## Generating a Coverage Report
1. `pytest --cov=. --cov-report term-missing`