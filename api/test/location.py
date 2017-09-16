from sqlalchemy import text
from api.db import db
from .fixtures import user
from faker import Faker


fake = Faker()
base_url = 'http://localhost:5000'


def test_create_location():
    body = {
        'owner_id': user.id,
        'name': fake.company()
    }

    response = user.post(base_url + '/v1/locations', json=body)

    assert response.status_code == 200

    query = text(
        'select * from location where name = \'' + body['name'] + '\'')
    assert db.engine.execute(query).rowcount == 1
