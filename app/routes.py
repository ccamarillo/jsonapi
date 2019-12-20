
from . import app, api
from flask import request
import grequests
import json
from flask_rest_jsonapi import Api
from .resources import UserList, UserDetail
import pprint

api = Api(app)
api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>')

@app.route('/batch', methods=['POST'])
def batch():
    requests = request.get_json()["data"]["requests"]

    rs = []
    for theRequest in requests:
        if theRequest["method"] == 'GET':
            rs.append(grequests.get(theRequest["url"]))
        if theRequest["method"] == 'POST':
            rs.append(grequests.post(theRequest["url"], json=theRequest))
        if theRequest["method"] == 'DELETE':
            rs.append(grequests.delete(theRequest["url"]))
        if theRequest["method"] == "PATCH":
            rs.append(grequests.patch(theRequest["url"], json=theRequest))
    
    responses = grequests.map(rs)
    
    responseJson = {
        "responses": []
    }

    
    for response in responses:
        app.logger.info(response.__dict__)
        theResponse = {}
        theResponse["method"] = response.request.method
        theResponse["url"] = response.url
        theResponse["status_code"] = response.status_code
        # For some reason flask-rest-jsonapi is not sending a "reason" attribute in the response
        if response.status_code == 404:
            reason = 'NOT FOUND'
        else:
            reason = response.reason
        theResponse["reason"] = reason
        theResponse["content"] = json.loads(response._content)
        responseJson["responses"].append(theResponse)

    return json.dumps(responseJson)