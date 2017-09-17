
# Authentication related functions.

from datetime import datetime
from .app import app
from functools import wraps
import jwt
from jwt.exceptions import DecodeError, InvalidTokenError
from flask import request, g
from .error import error


secret = app.config['JWT_SECRET']


def create_token(user):
    claim = {
        'email': user.email,
        'user_id': user.id,
        'roles': ['user'],
        'iat': datetime.utcnow()
    }
    return jwt.encode(claim, secret).decode('utf8')


def parse_token():

    header = request.headers.get('Authorization')

    if header is None:
        return error.unauthorized('Authorization header was not found')

    parts = header.split(' ')
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return error.unauthorized('Invalid authorization header format')

    try:
        g.jwt = jwt.decode(parts[1], secret)
    except (InvalidTokenError, DecodeError):
        return error.unauthorized('Please login')

    return None


def is_forbidden(required_roles, roles):
    for required in required_roles:
        if required in roles:
            return False

    return True


def authenticated(roles):

    def decorator(function):

        @wraps(function)
        def wrap(*args, **kwargs):
            error = parse_token()
            if error is None:
                if is_forbidden(roles, g.jwt['roles']):
                    return error.forbidden('Access is denied')
                else:
                    return function(*args, **kwargs)
            else:
                return error

        return wrap
    return decorator


def current_user():
    user = getattr(g, 'current_user', None)
    if user is None:

        raise Exception('There is no user in the current request context')

    return user


def current_user_id():
    return g.jwt['user_id']
