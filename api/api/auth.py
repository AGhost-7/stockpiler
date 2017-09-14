
# Authentication related functions.

from datetime import datetime
from .app import app
from functools import wraps
import jwt
from flask import request, jsonify, g
from http import HTTPStatus
from .models import User


secret = app.config['JWT_SECRET']


def create_token(user):
    claim = {
        'email': user.email,
        'iat': datetime.utcnow()
    }
    return jwt.encode(claim, secret).decode('utf8')


def authenticated(function):

    @wraps(function)
    def wrap():
        header = request.headers['Authorization']

        if header is None:
            body = {'message': 'header_not_found'}
            return jsonify(body), HTTPStatus.UNAUTHORIZED

        parts = header.split(' ')
        if len(parts) != 2 or parts[0] != 'Bearer':
            body = {'message': 'invalid_auth_header'}
            return jsonify(body), HTTPStatus.UNAUTHORIZED

        try:
            token = jwt.decode(parts[1], secret)
            g.current_user = User \
                .query \
                .filter(User.email == token.email) \
                .first()
        except (jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError):
            body = {'message': 'invalid_token'}
            return jsonify(body), HTTPStatus.UNAUTHORIZED

    return wrap


def current_user():
    user = getattr(g, 'current_user', None)
    if user is None:
        raise Exception('There is no user in the current request context')

    return user
