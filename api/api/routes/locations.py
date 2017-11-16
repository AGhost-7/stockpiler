from api.db import db
from api.models import User, Location, LocationMember, Item, ItemStock, \
    ItemLog, ItemStockLog
from api.auth import current_user_id
from api.error import error
from flask import Blueprint, request, jsonify, g
from api.validation import list_parser
from api.control import control
from uuid import uuid4

locations = Blueprint('locations', __name__, url_prefix='/v1/locations')


@locations.before_request
def prefetch_location():
    if 'location_id' in request.view_args:
        location_id = request.view_args['location_id']
        location = Location.query.get(location_id)
        if location_id is None:
            return error.not_found('Could not find location')
        g.location = location


@locations.route('', methods=['POST'])
@control.authorize(['user'])
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
@control.authorize(['user'])
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
@control.authorize(['owner'])
def add_location_member(location_id, member_id):
    member = LocationMember(user_id=member_id, location_id=location_id)
    db.session.add(member)
    db.session.commit()
    return jsonify(member.to_dict())


@locations.route('/<location_id>/members')
@control.authorize(['location'])
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
@control.authorize(['owner'])
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
@control.authorize(['location'])
def add_location_item(location_id):
    body = request.get_json()

    item = Item(name=body['name'], price=body['price'], version=str(uuid4()))
    db.session.add(item)
    db.session.flush()

    item_log = ItemLog(
        item_version=item.version,
        item_id=item.id,
        name=item.name,
        price=item.price
    )
    db.session.add(item_log)

    item_stock = ItemStock(
        item_id=item.id,
        location_id=location_id,
        quantity=body['quantity'],
        version=str(uuid4())
    )
    db.session.add(item_stock)
    db.session.flush()

    item_stock_log = ItemStockLog(
        item_id=item.id,
        item_version=item.version,
        item_stock_version=item_stock.version,
        location_id=item_stock.location_id,
        quantity=item_stock.quantity
    )
    db.session.add(item_stock_log)

    db.session.commit()

    return jsonify(item.with_stock(item_stock))


@locations.route('/<location_id>/items/<item_id>', methods=['PUT'])
@control.authorize(['location'])
def update_location_item(location_id, item_id):
    item_modified = False
    stock_modfied = False

    body = request.get_json()

    item = Item.query.get(item_id)
    if item.name != body['name'] or item.name != body['price']:
        item_modified = True
        last_version = item.version
        item.name = body['name']
        item.price = body['price']
        item.version = str(uuid4())
        db.session.add(item)

        item_log = ItemLog(
            item_version=item.version,
            last_item_version=last_version,
            item_id=item.id,
            name=item.name,
            price=item.price
        )
        db.session.add(item_log)

    item_stock = ItemStock \
        .query \
        .filter(ItemStock.item_id == item_id) \
        .first()

    if item_stock.quantity != body['quantity']:
        stock_modfied = True
        last_version = item_stock.version
        item_stock.version = str(uuid4())
        item_stock.quantity = body['quantity']
        db.session.add(item_stock)

        item_stock_log = ItemStockLog(
            item_id=item.id,
            item_version=item.version,
            item_stock_version=item_stock.version,
            last_item_stock_version=last_version,
            location_id=item_stock.location_id,
            quantity=body['quantity'])
        db.session.add(item_stock_log)

    db.session.commit()

    if not item_modified and not stock_modfied:
        return error.bad_request('Did not modify record.')
    else:
        return jsonify(item.with_stock(item_stock))


@locations.route('/<location_id>/items', methods=['GET'])
@control.authorize(['location'])
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
