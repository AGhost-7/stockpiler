
from flask_restful.reqparse import RequestParser


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
    parser = RequestParser()
    parser.add_argument('limit', default=20, location='args', type=limit)
    parser.add_argument(
        'offset', default=0, location='args', type=non_negative_int)
    return parser
