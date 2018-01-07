from test.util.session import create_session
from api.models import User
from requests_toolbelt import sessions


class UserFixture:
    def __init__(self, email, username, password):
        self.id = None
        self.email = email
        self.username = username
        self.password = password
        self.credentials = {
            'login': email,
            'password': password
        }
        self.requests = sessions.BaseUrlSession(
            base_url='http://localhost:5000')

    def ensure_created(self):
        with create_session() as session:
            db_user = session \
                .query(User) \
                .filter(User.email == self.email) \
                .first()
            if db_user is None:
                data = {
                    'username': self.username,
                    'email': self.email,
                    'password': self.password
                }
                response = self.requests.post(
                    '/v1/users/register', json=data)
                assert response.status_code == 200
                db_user = session \
                    .query(User) \
                    .filter(User.email == self.email) \
                    .first()
                db_user.email_confirmed = True
                self.id = db_user.id
            else:
                self.id = db_user.id

    def login(self):
        response = self.requests.post('/v1/users/login', json=self.credentials)
        assert response.status_code == 200
        self.requests.headers.update({
            'Authorization': 'bearer ' + response.json()['token']
        })


owner = UserFixture('aghost7@gmail.com', 'aghost7', 'password123')
employee = UserFixture('foo@bar.com', 'foobar', 'password')
snek = UserFixture('snek@tss', 'snek', '123')

users = [owner, employee, snek]

for user in users:
    user.ensure_created()
    user.login()
