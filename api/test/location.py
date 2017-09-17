from api.models import Location
from .fixtures import user
from faker import Faker
from .util.session import create_session


fake = Faker()
base_url = 'http://localhost:5000'

location_name = fake.company()


def test_create_location():
    body = {
        'owner_id': user.id,
        'name': location_name
    }

    response = user.post('/v1/locations', json=body)

    assert response.status_code == 200
    with create_session() as session:
        location = session \
            .query(Location) \
            .filter(Location.name == body['name']) \
            .first()
        assert location is not None


def test_list_own_locations():
    response = user.get('/v1/locations')
    locations = response.json()
    matches = [
        location
        for location in locations if location['name'] == location_name
    ]

    assert len(matches) == 1
