from api.models import Location
from .fixtures.user import owner, employee, snek
from faker import Faker
from .util.session import create_session
from .util.func import call_once


fake = Faker()
base_url = 'http://localhost:5000'

location_name = fake.company()
location_id = None


def test_create_location():
    body = {
        'owner_id': owner.id,
        'name': location_name
    }

    response = owner.requests.post('/v1/locations', json=body)

    assert response.status_code == 200
    with create_session() as session:
        location = session \
            .query(Location) \
            .filter(Location.name == body['name']) \
            .first()
        assert location is not None


def test_list_own_locations():
    response = owner.requests.get('/v1/locations?limit=100')
    assert response.status_code == 200
    locations = response.json()
    matches = [
        location
        for location in locations if location['name'] == location_name
    ]

    assert len(matches) == 1
    global location_id
    location_id = matches[0]['id']


def test_list_owner_locations_limit():
    response = owner.requests.get('/v1/locations?limit=200')
    assert response != 200


def test_add_location_member():
    response = owner.requests.post(
        '/v1/locations/' + location_id + '/members/' + employee.id)
    print(response.text)
    assert response.status_code == 200


def test_add_location_member_employee():
    response = employee.requests.post(
        '/v1/locations/' + location_id + '/members/' + snek.id)
    assert response.status_code == 403


def test_list_location_members():
    response = owner.requests.get(
        '/v1/locations/' + location_id + '/members')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_remove_location_members():
    response = owner.requests.delete(
        '/v1/locations/' + location_id + '/members/' + employee.id)
    assert response.status_code == 200
    response = owner.requests.get(
        '/v1/locations/' + location_id + '/members')

    assert len(response.json()) == 1


@call_once
def create_location_item():
    body = {
        'name': fake.text(),
        'quantity': fake.random_int(10 * 1000, 500 * 1000),
        'price': fake.random_number(6, 15) + fake.random_int(0, 100) / 100
    }
    response = owner.requests.post(
        '/v1/locations/' + location_id + '/items', json=body)
    assert response.status_code == 200
    return response.json()


def test_create_location_item():
    create_location_item()


def test_update_location_item():
    item = create_location_item()
    body = {
        'name': fake.text(),
        'quantity': fake.random_int(5, 10),
        'price': fake.random_int(20, 30) + fake.random_int(0, 100) / 100
    }
    response = owner.requests.put(
        '/v1/locations/' + location_id + '/items/' + item['id'], json=body)
    assert response.status_code == 200
    assert response.json()['quantity'] == body['quantity']


def test_list_location_item():
    response = owner.requests.get(
        '/v1/locations/' + location_id + '/items')
    assert response.status_code == 200
    item = response.json()[0]

    response = owner.requests.get(
        '/v1/locations/' + location_id + '/items?offset=1')
    assert response.status_code == 200
    offset_items = response.json()
    assert len(offset_items) == 0 or offset_items[0].id != item.id
