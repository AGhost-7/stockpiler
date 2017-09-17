from test.util.session import create_session
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

db_user = User.query.filter(User.email == email).first()

if db_user is None:
    body = {
        'email': email,
        'password': password
    }
    response = user.post('/v1/users/register', json=credentials)
    assert response.status_code == 200

    with create_session() as session:
        db_user = session \
            .query(User) \
            .filter(User.email == email) \
            .first()
        db_user.email_confirmed = True
        user.id = db_user.id
else:
    user.id = db_user.id

response = user.post('/v1/users/login', json=credentials)
assert response.status_code == 200

user.headers.update({
    'Authorization': 'bearer ' + response.json()['token']
})

user.email = email
user.password = password
user.id = db_user.id
