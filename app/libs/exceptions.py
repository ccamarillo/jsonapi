"""
Throw this when a custom validation rule failes for a request
"""


class ValidationException(Exception):
    def __init__(self, message, pointer=None):
        self.message = message
        if pointer != None:
            self.pointer = pointer
