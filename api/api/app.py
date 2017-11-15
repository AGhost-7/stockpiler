from os import environ
from flask_babel import Babel
from flask import Flask


app = Flask(__name__)

app.config['MAIL_DEFAULT_SENDER'] = 'noreply@api.com'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER', 'localhost')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/test')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET'] = 'shhh'

babel = Babel(app)
