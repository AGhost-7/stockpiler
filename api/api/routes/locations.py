from api.db import db
from api.models import User, Location, LocationMember, Item, ItemStock
from api.auth import authenticated, current_user_id
from api.error import error
from flask import Blueprint, request, jsonify
from api.validation import list_parser


locations = Blueprint('locations', __name__, url_prefix='/v1/locations')


@locations.route('', methods=['POST'])
@authenticated(['user'])
def create_location():
    body = request.get_json()
    owner_id = body['owner_id']

    user = User.query.get(owner_id)

    if user is None:
        return error.not_found('User not found')

    location = Location(owner_id=user.id, name=body['name'])

    db.session.add(location)
    db.session.commit()

    return jsonify(location.to_dict())


@locations.route('', methods=['GET'])
@authenticated(['user'])
def list_locations():
    parser = list_parser()
    args = parser.parse_args()
    user_id = current_user_id()
    locations = Location \
        .query \
        .outerjoin(LocationMember) \
        .filter(
            LocationMember.user_id == user_id or
            Location.owner_id == user_id) \
        .offset(args['offset']) \
        .limit(args['limit']) \
        .all()

    return jsonify([location.to_dict() for location in locations])


@locations.route('/<location_id>/members/<member_id>', methods=['POST'])
@authenticated(['user'])
def add_location_member(location_id, member_id):
    location = Location.query.get(location_id)
    if location is None:
        return error.not_found('Invalid location')
    if location.owner_id != current_user_id():
        return error.unauthorized(
            'Cannot modify location members unless owner of location')
    else:
        member = LocationMember(user_id=member_id, location_id=location_id)
        db.session.add(member)
        db.session.commit()
        return jsonify(member.to_dict())


@locations.route('/<location_id>/members')
@authenticated(['user'])
def list_location_members(location_id):
    parser = list_parser()
    args = parser.parse_args()
    members = User \
        .query \
        .join(LocationMember, LocationMember.user_id == User.id) \
        .filter(LocationMember.location_id == location_id) \
        .offset(args['offset']) \
        .limit(args['limit']) \
        .all()

    return jsonify([member.to_dict() for member in members])


@locations.route('/<location_id>/members/<member_id>', methods=['DELETE'])
@authenticated(['user'])
def delete_location_member(location_id, member_id):
    affected_records = LocationMember \
        .query \
        .filter(
            LocationMember.location_id == location_id
            and LocationMember.user_id == member_id) \
        .delete()

    if affected_records < 1:
        return error.not_found(
            'Cannot delete user as he is not a member of the location')
    return ('', 200)


@locations.route('/<location_id>/items', methods=['POST'])
@authenticated(['user'])
def add_location_item(location_id):
    body = request.get_json()

    item = Item(name=body['name'], price=body['price'])
    db.session.add(item)
    db.session.flush()

    item_stock = ItemStock(
        item_id=item.id, location_id=location_id, quantity=body['quantity'])
    db.session.add(item_stock)
    db.session.commit()

    return jsonify(item.with_stock(item_stock))


@locations.route('/<location_id>/items/<item_id>', methods=['PUT'])
@authenticated(['user'])
def update_location_item(location_id, item_id):
    body = request.get_json()

    item = Item.query.get(item_id)
    item.name = body['name']
    item.price = body['price']
    db.session.add(item)

    item_stock = ItemStock \
        .query \
        .filter(ItemStock.item_id == item_id) \
        .first()
    item_stock.quantity = body['quantity']
    db.session.add(item)

    db.session.commit()

    return jsonify(item.with_stock(item_stock))


@locations.route('/<location_id>/items', methods=['GET'])
@authenticated(['user'])
def list_location_items(location_id):
    parser = list_parser()
    args = parser.parse_args()
    items = db \
        .session \
        .query(Item, ItemStock) \
        .join(ItemStock) \
        .filter(ItemStock.location_id == location_id) \
        .limit(args['limit']) \
        .offset(args['offset']) \
        .all()

    result = [item.with_stock(item_stock) for (item, item_stock) in items]

    return jsonify(result)
