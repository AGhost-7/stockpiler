from datetime import datetime
from sqlalchemy import Column, String, Boolean, BLOB, ForeignKey, DateTime
from sqlalchemy.sql import func as sqlfunc
from .db import db


def Id():
    return Column(String(36), primary_key=True)


class ChangeTracked:
    created_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now(),
        onupdate=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'user'
    id = Id()
    email = Column(String(256), nullable=False, unique=True)
    password = Column(BLOB(60), nullable=False)
    email_confirmed = Column(Boolean(), nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'email_confirmed': self.email_confirmed
        }


class EmailConfirmation(db.Model):
    __tablename__ = 'email_confirmation'
    id = Id()
    user_id = Column(ForeignKey('user.id'), nullable=False)


class Location(db.Model, ChangeTracked):
    __tablename__ = 'location'

    id = Id()
    owner_id = Column(ForeignKey('user.id'), nullable=False)
    name = Column(String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name
        }
