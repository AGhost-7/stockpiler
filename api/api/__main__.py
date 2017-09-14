
import bcrypt
from .db import db
from .app import app
from uuid import uuid4
from .models import User, EmailConfirmation
from flask import request, jsonify
from .mail import send_mail
from http import HTTPStatus
from .auth import create_token


@app.route('/v1/users/register', methods=['POST'])
def register():
    body = request.get_json()
    email = body['email']

    hashed = bcrypt.hashpw(bytes(body['password'], 'utf8'), bcrypt.gensalt())
    user = User(id=str(uuid4()), email=email, password=hashed)
    db.session.add(user)
    db.session.flush()

    confirmation = EmailConfirmation(id=str(uuid4()), user_id=user.id)
    db.session.add(confirmation)

    send_mail('confirm-email', [email], id=confirmation.id)
    db.session.commit()

    return jsonify(user.to_dict())


@app.route('/v1/users/confirm-email/<id>')
def confirm_email(id):
    confirmation = EmailConfirmation.query.get(id)
    if confirmation is None:
        response = jsonify({'error': 'link-invalid'})
        response.status_code = HTTPStatus.NOT_FOUND.value
        return response
    else:
        user = User.query.get(confirmation.user_id)
        user.email_confirmed = True
        db.session.delete(confirmation)
        db.session.commit()
        return jsonify(user.to_dict())


@app.route('/v1/users/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User \
        .query \
        .filter(User.email == email) \
        .first()

    if user is None:
        return jsonify({'message': 'email_invalid'}), HTTPStatus.NOT_FOUND

    if not user.email_confirmed:
        body = {'message': 'email_not_confirmed'}
        return jsonify(body), HTTPStatus.BAD_REQUEST

    if not bcrypt.checkpw(bytes(password, 'utf8'), user.password):
        body = {'message': 'incorrect_password'}
        return jsonify(body), HTTPStatus.BAD_REQUEST

    return jsonify({'token': create_token(user)})


app.run(debug=True)
