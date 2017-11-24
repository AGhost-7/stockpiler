
from flask_restful import reqparse
from flask_restful.reqparse import RequestParser
from flask import jsonify


def on_validation_error(error):
    response = jsonify({'message': error.message})
    response.status_code = error.status_code
    return response


class ValidationError(Exception):
    status_code = 400

    def __init__(self, message):
        self.message = message
        super(ValidationError, self).__init__()


class ArgValidator(reqparse.Argument):
    def handle_validation_error(self, message, bundle_errors):
        ex = ValidationError(str(message))
        raise ex


def non_negative_int(value):
    try:
        value = int(value)
    except Exception():
        raise TypeError('Must be an integer')
    if value < 0:
        raise ValueError('Number cannot be less than zero')
    return value


def limit(value):
    value = non_negative_int(value)
    if value > 100:
        raise ValueError('Limit cannot be greater than 100')
    return value


def list_parser():
    parser = RequestParser(argument_class=ArgValidator)
    parser.add_argument('limit', default=20, location='args', type=limit)
    parser.add_argument(
        'offset', default=0, location='args', type=non_negative_int)
    return parser


def simple_parser():
    return RequestParser(argument_class=ArgValidator)
