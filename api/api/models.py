from .db import db
from datetime import datetime
from sqlalchemy import Column, String, Boolean, BLOB, ForeignKey, DateTime, \
    PrimaryKeyConstraint
from sqlalchemy.sql import func as sqlfunc


def Id():
    return Column(String(36), primary_key=True)


class TrackUpdator:
    updated_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now(),
        onupdate=datetime.utcnow)


class TrackCreator:
    created_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now())


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


class Location(db.Model, TrackCreator, TrackUpdator):
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


class LocationMember(db.Model, TrackCreator):
    __tablename__ = 'location_access'

    location_id = Column(ForeignKey('location.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    __table_args__ = (PrimaryKeyConstraint(location_id, user_id),)

    def to_dict(self):
        return {
            'location_id': self.location_id,
            'user_id': self.user.id
        }


def drop_all():
    db.drop_all()


def create_all():
    db.create_all()
