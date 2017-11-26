
from flask_babel import gettext
from flask import jsonify, request


class ValidationError(Exception):
    def __init__(self, errors, status_code=404):
        self.errors = errors
        self.status_code = 404


class RequestParser(object):
    def __init__(self):
        self.errors = {}
        self.args = {}

    def _is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, str) and len(value.strip()) == 0:
            return True
        return False

    def add_argument(
            self, key, location=('json', 'values'), required=False, type=str,
            default=None):

        try:
            if isinstance(location, str):
                value = getattr(request, location).get(key, default)
                if required and self._is_empty(value):
                    self.errors[key] = gettext('Field is required')
                else:
                    self.args[key] = type(value)
            else:
                value = default
                for item in location:
                    prop = getattr(request, item)
                    if key in prop:
                        value = prop[key]
                        if value is not None:
                            self.args[key] = type(value)
                if required and self._is_empty(value):
                    self.errors[key] = gettext('Field is required')
        except ValueError as err:
            self.errors[key] = gettext(str(err))
        except TypeError as err:
            self.errors[key] = gettext(str(err))
        return self

    def parse_args(self):
        if self.errors:
            raise ValidationError(self.errors)
        else:
            return self.args


def on_validation_error(error):
    response = jsonify({'errors': error.errors})
    response.status_code = error.status_code
    return response


def non_negative_int(value):
    try:
        value = int(value)
    except Exception as e:
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


def simple_parser():
    return RequestParser()
