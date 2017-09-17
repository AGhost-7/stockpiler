from uuid import uuid4
from api.db import db
from api.models import User, Location, LocationMember
from api.auth import authenticated, current_user_id
from api.error import error
from flask import Blueprint, request, jsonify


locations = Blueprint('locations', __name__, url_prefix='/v1/locations')


@locations.route('', methods=['POST'])
@authenticated(['user'])
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


@locations.route('', methods=['GET'])
@authenticated(['user'])
def list_locations():
    user_id = current_user_id()
    locations = Location \
        .query \
        .outerjoin(LocationMember) \
        .filter(
            LocationMember.user_id == user_id or
            Location.owner_id == user_id) \
        .all()

    return jsonify([location.to_dict() for location in locations])


@locations.route('<location_id>/members/<member_id>', methods=['POST'])
@authenticated(['user'])
def add_location_member(location_id, member_id):
    location = Location.query.get(location_id)
    if location is None:
        return error.bad_request('Invalid location')
    if location.owner_id != current_user_id():
        return error.unauthorized(
            'Cannot modify location members unless owner of location')
    else:
        member = LocationMember(user_id=member_id, location_id=location_id)
        db.session.add(member)
        db.session.commit()
        return jsonify(member.to_dict())
