from api.models import User
import requests


def by_email(email):
    return User \
        .query \
        .filter(User.email == email) \
        .first()


email = 'aghost7@gmail.com'
password = 'password123'

user = by_email(email)
print('user is currently', user.to_dict())

if user is None:
    body = {
        'email': email,
        'password': password
    }
    response = requests.post(
        'http://localhost:5000/v1/users/register', json=body)
    assert response.status_code == 200
    print('registered:', response.json())

    user = by_email(email)
    print('user is', user)
    user.email_confirmed = True

    user.commit()
