import bcrypt
from api.error import error
from api.db import db
from api.models import User, EmailConfirmation
from flask import request, jsonify, Blueprint
from api.mail import send_mail
from api.auth import create_token
from api.config import config


users = Blueprint('users', __name__, url_prefix='/v1/users')


@users.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    email = body['email']

    hashed = bcrypt.hashpw(bytes(body['password'], 'utf8'), bcrypt.gensalt())
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
    confirmation = EmailConfirmation.query.get(id)
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
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User \
        .query \
        .filter(User.email == email) \
        .first()

    if user is None:
        return error.not_found('Could not find a user tied to the given email')

    if not user.email_confirmed:
        return error.bad_request('Email confirmation is still pending')

    if not bcrypt.checkpw(bytes(password, 'utf8'), user.password):
        return error.bad_request('Incorrect password')

    return jsonify({'token': create_token(user)})
