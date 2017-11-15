
from os import environ

config = {
    'MAIL_DEFAULT_SENDER': 'noreply@api.com',
    'MAIL_PORT': 1025,
    'MAIL_SERVER': environ.get('MAIL_SERVER', 'localhost'),

    'SQLALCHEMY_DATABASE_URI': environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:root@localhost:3306/test'),
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'JWT_SECRET': 'shhh',
    'BASE_URL': environ.get('BASE_URL', 'localhost')
}
