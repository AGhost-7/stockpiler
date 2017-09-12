import requests
from faker import Faker
from api.models import User


fake = Faker()


base_url = 'http://localhost:5000'
# This is actually the http api that mailhog exposes.
mail_base_url = 'http://localhost:8025'


def test_user_registration():
    requests.delete(mail_base_url + '/api/v1/messages')
    data = {
        'email': fake.email(),
        'password': fake.password()
    }

    response = requests.post(base_url + '/v1/users/register', json=data)
    assert response.json()['email'] == data['email']

    response = requests.get(mail_base_url + '/api/v1/messages')
    assert len(response.json()) == 1

    user = User.query.filter(User.email == data['email']).first()
    assert user is not None
    assert user.active is not True
    assert user.password != data['password']
