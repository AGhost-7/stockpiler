from sqlalchemy import Column, String, Boolean, BLOB, ForeignKey
from .db import db


def Id():
    return Column(String(36), primary_key=True)


class User(db.Model):
    __tablename__ = 'user'
    id = Id()
    email = Column(String(256), nullable=False)
    password = Column(BLOB(60), nullable=False)
    active = Column(Boolean(), nullable=False, default=False)


class EmailConfirmation(db.Model):
    __tablename__ = 'email_confirmation'
    id = Id()
    user_id = Column(ForeignKey('user.id'), nullable=False)
