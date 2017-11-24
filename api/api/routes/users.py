import bcrypt
from api.error import error
from api.db import db
from api.models import User, EmailConfirmation, PasswordReset
from flask import jsonify, Blueprint
from api.mail import send_mail
from api.auth import create_token
from api.config import config
from api.validation import simple_parser
from flask_babel import gettext

users = Blueprint('users', __name__, url_prefix='/v1/users')


@users.route('/register', methods=['POST'])
def register():
    args = simple_parser() \
        .add_argument('email', type=str, required=True) \
        .add_argument('password', type=str, required=True) \
        .parse_args()

    email = args['email']

    if User.by_email(email) is not None:
        return error.bad_request(
            'A user with the given email already exists.')

    hashed = bcrypt.hashpw(bytes(args['password'], 'utf8'), bcrypt.gensalt())
    user = User(email=email, password=hashed)
    db.session.add(user)
    db.session.flush()

    confirmation = EmailConfirmation(user_id=user.id)
    db.session.add(confirmation)

    db.session.commit()
    confirmation_url = config['BASE_URL'] + '/email-confirmation/' + \
        confirmation.id

    send_mail('confirm-email', [email], confirmation_url=confirmation_url)

    return jsonify(user.to_dict())


@users.route('/confirm-email/<id>')
def confirm_email(id):
    args = simple_parser() \
        .add_argument('id', type=str, required=True, location='view_args') \
        .parse_args()

    confirmation = EmailConfirmation.query.get(args['id'])
    if confirmation is None:
        return error.not_found('Link is invalid')
    else:
        user = User.query.get(confirmation.user_id)
        user.email_confirmed = True
        db.session.delete(confirmation)
        db.session.commit()
        return jsonify(user.to_dict())


@users.route('/login', methods=['POST'])
def login():
    args = simple_parser() \
        .add_argument('email', type=str, required=True) \
        .add_argument('password', type=str, required=True) \
        .parse_args()

    email = args['email']
    password = args['password']

    user = User.by_email(email)

    if user is None:
        return error.not_found('Could not find a user tied to the given email')

    if not user.email_confirmed:
        return error.bad_request('Email confirmation is still pending')

    if not bcrypt.checkpw(bytes(password, 'utf8'), user.password):
        return error.bad_request('Incorrect password')

    return jsonify({'token': create_token(user)})


@users.route('/password-reset', methods=['POST'])
def request_password_reset():
    args = simple_parser() \
        .add_argument('email', type=str, required=True) \
        .parse_args()

    user = User.by_email(args['email'])
    if user is None:
        return error.not_found(
            'Email %(email)s is invalid.', email=args['email'])

    old_reset = PasswordReset \
        .query \
        .filter(PasswordReset.user_id == user.id) \
        .first()

    message = gettext('Email sent.')
    if old_reset is not None:
        db.session.delete(old_reset)
        db.session.flush()
        message = gettext('Password reset re-sent.')

    reset = PasswordReset(user_id=user.id)
    db.session.add(reset)

    db.session.commit()

    reset_url = config['BASE_URL'] + '/password-reset/' + reset.token

    send_mail('password-reset', [user.email], reset_url=reset_url)

    return jsonify({'message': message})


def password_reset_errors(reset):
    if reset is None:
        return error.not_found(
            'Password reset is not valid.')

    if reset.is_expired():
        return error.bad_request(
            'Your password reset has expired. Please send another request.')


@users.route('/password-reset/<token>', methods=['GET'])
def validate_password_reset(token):
    args = simple_parser() \
        .add_argument('token', type=str, location='view_args', required=True) \
        .parse_args()

    reset = PasswordReset.by_token(args['token'])

    error = password_reset_errors(reset)
    if error:
        return error
    else:
        user = User.query.get(reset.user_id)
        body = reset.to_dict()
        body['user'] = user.to_dict()
        return jsonify(body)


@users.route('/password-reset/<token>', methods=['POST'])
def submit_password_reset(token):
    args = simple_parser() \
        .add_argument('token', type=str, location='view_args', required=True) \
        .add_argument('password', type=str, required=True) \
        .parse_args()

    reset = PasswordReset.by_token(args['token'])
    error = password_reset_errors(reset)
    if error:
        return error

    user = User.query.get(reset.user_id)
    user.password = bcrypt.hashpw(
        bytes(args['password'], 'utf8'), bcrypt.gensalt())
    db.session.add(user)
    db.session.delete(reset)
    db.session.commit()

    return jsonify(user.to_dict())
