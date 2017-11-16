import requests
from faker import Faker
from api.models import User, EmailConfirmation
from .util.session import create_session
from os import environ
import re

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
    with create_session() as session:
        user = session.query(User).filter(User.email == state['email']).first()
        assert user is not None
        assert user.email_confirmed is not True
        assert user.password != state['password']


def test_user_registration_email():
    response = requests.get(mail_base_url + '/api/v1/messages')
    messages = response.json()
    assert len(messages) == 1
    email_body = messages[0]['MIME']['Parts'][0]['MIME']['Parts'][0]['Body']
    id = re.findall('.+/email-confirmation/([a-z0-9-]+)', email_body)[0]
    with create_session() as session:
        confirmation = session.query(EmailConfirmation).get(id)
        assert confirmation is not None
    state['confirmation_id'] = id


def test_user_confirmation():
    response = requests.get(
        base_url + '/v1/users/confirm-email/boom')
    assert response.status_code >= 400

    response = requests.get(
        base_url + '/v1/users/confirm-email/' + state['confirmation_id'])
    assert response.status_code == 200


def test_user_login():
    response = requests.post(base_url + '/v1/users/login', json=state)
    assert response.status_code == 200
    body = response.json()
    assert 'token' in body
