from api.config import config
from .db import db
from datetime import datetime
from sqlalchemy import Column, Boolean, ForeignKey, DateTime, \
    PrimaryKeyConstraint, Integer, Numeric, Text, String, UniqueConstraint, or_
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql import func as sqlfunc
from uuid import uuid4


def uuid():
    return str(uuid4())


def Id():
    return Column(String(36), primary_key=True, default=uuid)


def Uuid():
    return String(36)


class TrackUpdates:
    updated_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now(),
        onupdate=datetime.utcnow)


class TrackCreations:
    created_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now())


class User(db.Model):
    __tableargs__ = (UniqueConstraint('email', 'username'),)
    id = Id()
    email = Column(Text(), nullable=False, unique=True)
    password = Column(BYTEA(60), nullable=False)
    username = Column(Text(), nullable=False, unique=True)
    email_confirmed = Column(Boolean(), nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'email_confirmed': self.email_confirmed
        }

    def by_email(email):
        return User.query.filter(User.email == email).first()

    def by_login(*values):
        return User \
            .query \
            .filter(or_(User.email.in_(values), User.username.in_(values))) \
            .first()


class EmailConfirmation(db.Model, TrackCreations):
    id = Id()
    user_id = Column(ForeignKey('user.id'), nullable=False)


class PasswordReset(db.Model, TrackCreations):
    user_id = Column(ForeignKey('user.id'), nullable=False)
    token = Column(Text(), default=uuid, nullable=False)
    __table_args__ = (PrimaryKeyConstraint(user_id),)

    def is_expired(self):
        ttl = config['PASSWORD_RESET_TTL_SECONDS']
        seconds_elapsed = (datetime.now() - self.created_at).total_seconds()
        return seconds_elapsed > ttl

    def to_dict(self):
        return {
            'token': self.token,
            'user_id': self.user_id
        }

    def by_token(token):
        return PasswordReset.query.filter(PasswordReset.token == token).first()


class Location(db.Model, TrackCreations, TrackUpdates):

    id = Id()
    owner_id = Column(ForeignKey('user.id'), nullable=False)
    name = Column(Text(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name
        }


class LocationMember(db.Model, TrackCreations):

    location_id = Column(ForeignKey('location.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    __table_args__ = (PrimaryKeyConstraint(location_id, user_id),)

    def to_dict(self):
        return {
            'location_id': self.location_id,
            'user_id': self.user_id
        }


class Item(db.Model, TrackCreations, TrackUpdates):
    id = Id()
    version = Column(Uuid())
    name = Column(Text, nullable=False)
    price = Column(Numeric(15, 2))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

    def with_stock(self, stock):
        item = self.to_dict()
        item['location_id'] = stock.location_id
        item['quantity'] = stock.quantity
        return item


# Split into two tables to avoid having migration pains when I add orgs.
class ItemStock(db.Model, TrackCreations, TrackUpdates):

    item_id = Column(ForeignKey('item.id'), nullable=False)
    location_id = Column(ForeignKey('location.id'), nullable=False)
    version = Column(Uuid())
    # Quantity for now is in milligrams. Will add enum later...
    quantity = Column(Integer, nullable=False)
    # Price of an item stock will be coalesced from the item.
    price = Column(Numeric(15, 2))
    __tableargs__ = (PrimaryKeyConstraint(item_id, location_id),)


class ItemLog(db.Model, TrackCreations):
    item_version = Column(Uuid(), unique=True)
    last_item_version = Column(Uuid())
    item_id = Column(ForeignKey('item.id'), nullable=False)

    name = Column(Text(), nullable=False)
    price = Column(Numeric(15, 2))

    __table_args__ = (PrimaryKeyConstraint(item_id, item_version),)


class ItemStockLog(db.Model, TrackCreations):
    item_id = Column(ForeignKey('item.id'), nullable=False)
    item_version = Column(ForeignKey('item_log.item_version'), nullable=False)

    item_stock_version = Column(Uuid())
    last_item_stock_version = Column(Uuid())

    location_id = Column(ForeignKey('location.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(15, 2))

    __table_args__ = (PrimaryKeyConstraint(item_id, item_stock_version),)


def drop_all():
    db.drop_all()


def create_all():
    db.create_all()
