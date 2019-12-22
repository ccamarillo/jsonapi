from . import app
from .libs.exceptions import ValidationException
from jsonschema.exceptions import ValidationError

import json
from werkzeug.exceptions import InternalServerError


@app.errorhandler(404)
def not_found(error):
    return json.dumps(get_standard_error(404, "Not found")), 404


@app.errorhandler(500)
def internal_error(error):
    return json.dumps(get_standard_error(500, "An internal error occured.")), 500


@app.errorhandler(Exception)
def handle_exception(error):
    return (
        json.dumps(get_standard_error(500, "An internal error occured.", print(error))),
        500,
    )


@app.errorhandler(InternalServerError)
def handle_exception(error):
    return (
        json.dumps(get_standard_error(500, "An internal error occured.", print(error))),
        500,
    )


@app.errorhandler(ValidationException)
def handle_exception(error):
    return (
        json.dumps(
            get_standard_error(
                422, "A validation error occured.", error.message, error.pointer
            )
        ),
        422,
    )


@app.errorhandler(ValidationError)
def validation_error(error):
    pathItems = []
    for pathItem in error.path:
        pathItems.append(str(pathItem))
    return (
        get_standard_error(
            422, "Validation error", error.message, "/" + "/".join(pathItems)
        ),
        422
    )


def get_standard_error(status, title, message=None, pointer=None):
    error = {"errors": [{"title": title}]}
    if message != None:
        error["errors"][0]["detail"] = message
    if pointer != None:
        error["errors"][0]["source"] = {"pointer": pointer}
    return error
