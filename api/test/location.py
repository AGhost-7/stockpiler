import requests
from api.models import Location
from .fixtures import user
from faker import Faker


fake = Faker()
base_url = 'http://localhost:5000'


def test_create_location():
    body = {
        'owner_id': user.id,
        'name': fake.company()
    }

    response = requests.post(base_url + '/v1/locations', json=body)

    print('location response:', response.text)
    assert response.status_code == 200

    location = Location \
        .query \
        .filter(Location.name == body['name']) \
        .first()

    assert location is not None
