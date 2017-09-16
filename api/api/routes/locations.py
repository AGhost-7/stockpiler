from uuid import uuid4
from api.db import db
from api.models import User, Location
from api.auth import authenticated
from api.error import error
from flask import Blueprint, request, jsonify


locations = Blueprint('locations', __name__, url_prefix='/v1/locations')


@locations.route('', methods=['POST'])
@authenticated
def create_location():
    body = request.get_json()
    owner_id = body['owner_id']

    user = User.query.get(owner_id)

    if user is None:
        return error.not_found('User not found')

    location = Location(id=str(uuid4()), owner_id=user.id, name=body['name'])

    db.session.add(location)
    db.session.commit()

    return jsonify(location.to_dict())
