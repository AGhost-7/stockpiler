
import bcrypt
from .db import db
from .app import app
from uuid import uuid4
from .models import User, EmailConfirmation
from flask import request, jsonify
from .mail import send_mail
from http import HTTPStatus


@app.route('/v1/users/register', methods=['POST'])
def register():
    body = request.get_json()
    email = body['email']

    hashed = bcrypt.hashpw(bytes(body['password'], 'utf8'), bcrypt.gensalt())
    user = User(id=str(uuid4()), email=email, password=hashed)
    db.session.add(user)

    confirmation = EmailConfirmation(id=str(uuid4()), user_id=user.id)
    db.session.add(confirmation)

    send_mail('confirm-email', [email], id=confirmation.id)
    db.session.commit()

    return jsonify({'email': body['email'], 'active': False})


@app.route('/v1/users/confirm-email/<id>')
def confirm_email(id):
    confirmation = EmailConfirmation.query.get(id)
    if confirmation is None:
        response = jsonify({'error': 'link-invalid'})
        response.status_code = HTTPStatus.NOT_FOUND.value
        return response
    else:
        user = User.query.get(confirmation.user_id)
        user.active = True
        db.session.delete(confirmation)
        db.session.commit()
        return jsonify({'email': user.email, 'active': True})


app.run(debug=True)
