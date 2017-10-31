import requests
from faker import Faker
from api.models import User, EmailConfirmation
from os import environ

fake = Faker()


base_url = 'http://localhost:5000'
# This is actually the http api that mailhog exposes.
mail_base_url = 'http://' + environ.get('MAIL_SERVER', 'localhost') + ':8025'

state = {
    'email': fake.email(),
    'password': fake.password()
}


def test_clean_emails():
    response = requests.delete(mail_base_url + '/api/v1/messages')
    assert response.status_code == 200


def test_user_registration():
    response = requests.post(base_url + '/v1/users/register', json=state)
    assert response.status_code == 200
    assert response.json()['email'] == state['email']

    user = User.query.filter(User.email == state['email']).first()
    assert user is not None
    assert user.email_confirmed is not True
    assert user.password != state['password']


def test_user_registration_email():
    response = requests.get(mail_base_url + '/api/v1/messages')
    messages = response.json()
    assert len(messages) == 1
    email_body = messages[0]['MIME']['Parts'][0]['MIME']['Parts'][0]['Body']
    id = email_body.split('\n')[1]

    confirmation = EmailConfirmation.query.get(id)
    assert confirmation is not None
    state['confirmation_id'] = confirmation.id


def test_user_confirmation():
    def assert_response(id, status):
        response = requests.get(
            base_url + '/v1/users/confirm-email/' + id)

        assert response.status_code == status

    assert_response('booom', 404)
    assert_response(state['confirmation_id'], 200)


def test_user_login():
    response = requests.post(base_url + '/v1/users/login', json=state)
    assert response.status_code == 200
    body = response.json()
    assert 'token' in body
