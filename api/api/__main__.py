
import bcrypt
from .db import db
from .app import app
from uuid import uuid4
from .models import User
from flask import request, jsonify
from .mail import mail


@app.route('/v1/users/register', methods=['POST'])
def register():
    body = request.get_json()
    hashed = bcrypt.hashpw(bytes(body['password'], 'utf8'), bcrypt.gensalt())
    user = User(id=str(uuid4()), email=body['email'], password=hashed)
    db.session.add(user)
    db.session.commit()
    mail.send_message('hello', recipients=[body['email']])
    return jsonify({'email': body['email'], 'active': False})


app.run(debug=True)
