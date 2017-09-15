
# Module for handling translated error messages. All http statuses should be
# available.
# Usage:
# error.unauthorized('EYYY gotta login m8')

from http import HTTPStatus
from flask import jsonify
from flask_babel import gettext


class HTTPErrors:
    pass


def create_property(prop):
    status = getattr(HTTPStatus, prop)

    def http_error(self, message):
        body = {'message': gettext(message)}
        return jsonify(body), status.value

    lower = status.name.lower()
    http_error.__name__ = lower
    setattr(HTTPErrors, lower, http_error)


for prop in dir(HTTPStatus):
    if not prop.startswith('__'):
        create_property(prop)

error = HTTPErrors()
