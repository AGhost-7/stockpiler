
from os import environ, urandom


def get_bool(key, default):
    if key in environ:
        value = environ[key].lower()
        if value in ['1', 'true']:
            return True
        elif value in ['0', 'false']:
            return False
        else:
            message = 'Invalid value "{}" for boolean parameter: {}' \
                .format(key, environ[key])
            raise ValueError(message)
    else:
        return default


def get_int(key, default):
    if key in environ:
        return int(environ[key])
    else:
        return default


config = {

    'MAIL_SERVER': environ.get('MAIL_SERVER', 'localhost'),
    'MAIL_PORT': get_int('MAIL_PORT', 1025),
    'MAIL_USERNAME': environ.get('MAIL_USERNAME'),
    'MAIL_PASSWORD': environ.get('MAIL_PASSWORD'),
    'MAIL_DEFAULT_SENDER': environ.get(
        'MAIL_DEFAULT_SENDER', 'noreply@stockpiler.ca'),
    'MAIL_USE_TLS': get_bool('MAIL_USE_TLS', False),

    'SQLALCHEMY_DATABASE_URI': environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql+psycopg2://postgres:test@localhost:5432/test'),
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    'JWT_SECRET': environ.get('JWT_SECRET', urandom(20).hex()),
    'BASE_URL': environ.get('BASE_URL', 'localhost:3000'),
    'PASSWORD_RESET_TTL_SECONDS': 60 * 60,
    'DEBUG': get_bool('DEBUG', True)
}
