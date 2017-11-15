
# Access control logic

from flask import request, g
from functools import wraps
from api.models import LocationMember, Location
from api.auth import parse_token, current_user_id
from api.error import error


class AccessControl:
    def __init__(self):
        self.grants = {}

    def grant(self, grant_key):
        def store(function):
            self.grants[grant_key] = function
        return store

    def _is_granted_access(self, grant_keys):
        result = None
        for grant_key in grant_keys:
            grant = self.grants[grant_key]
            result = grant()
            if result is None:
                break
        return result

    def authorize(self, grant_keys):
        def decorator(function):

            @wraps(function)
            def wrap(*args, **kwargs):
                error = parse_token()
                if error is None:
                    error = self._is_granted_access(grant_keys)
                    if error is None:
                        return function(*args, **kwargs)

                return error

            return wrap

        return decorator


control = AccessControl()


@control.grant('user')
def user_grant():
    if 'user' not in g.jwt['roles']:
        return error.forbidden('Must be authenticated as a user')


@control.grant('location')
def location_grant():
    user_id = current_user_id()
    location_id = request.view_args['location_id']
    location = Location \
        .query \
        .outerjoin(
            LocationMember, LocationMember.location_id == location_id) \
        .filter(
            LocationMember.user_id == user_id or Location.owner_id == user_id
        ) \
        .first()

    if location is None:
        return error.forbidden('Not a member of location')


@control.grant('owner')
def owner_grant():
    user_id = current_user_id()
    location_id = request.view_args['location_id']
    location = Location.query.get(location_id)

    if location is None:
        return error.bad_request('Location does not exist')
    if location.owner_id != user_id:
        return error.forbidden(
            'Must be owner of the location to perform action')
