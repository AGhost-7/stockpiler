from api.models import User
from requests_toolbelt import sessions


def by_email(email):
    return User \
        .query \
        .filter(User.email == email) \
        .first()


email = 'aghost7@gmail.com'
password = 'password123'

credentials = {
    'email': email,
    'password': password
}
user = sessions.BaseUrlSession(base_url='http://localhost:5000')

db_user = by_email(email)

if db_user is None:
    body = {
        'email': email,
        'password': password
    }
    response = user.post('/v1/users/register', json=credentials)
    assert response.status_code == 200

    db_user = by_email(email)
    db_user.email_confirmed = True

    db_user.commit()

response = user.post('/v1/users/login', json=credentials)
assert response.status_code == 200

user.headers.update({
    'Authorization': 'bearer ' + response.json()['token']
})

user.email = email
user.password = password
user.id = db_user.id
