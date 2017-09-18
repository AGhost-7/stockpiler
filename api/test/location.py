from api.models import Location
from .fixtures.user import owner, employee
from faker import Faker
from .util.session import create_session


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
    response = owner.requests.get('/v1/locations')
    locations = response.json()
    matches = [
        location
        for location in locations if location['name'] == location_name
    ]

    assert len(matches) == 1
    global location_id
    location_id = matches[0]['id']


def test_add_location_member():
    print('location_id', location_id, 'employee.id', employee.id)
    response = owner.requests.post(
        '/v1/locations/' + location_id + '/members/' + employee.id)
    assert response.status_code == 200


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
