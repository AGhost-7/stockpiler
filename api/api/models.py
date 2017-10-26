from .db import db
from datetime import datetime
from sqlalchemy import Column, String, Boolean, BLOB, ForeignKey, DateTime, \
    PrimaryKeyConstraint, Integer, Numeric
from sqlalchemy.sql import func as sqlfunc
from uuid import uuid4


def create_id():
    return str(uuid4())


def Id():
    return Column(String(36), primary_key=True, default=create_id)


class TrackUpdates:
    updated_at = Column(
        DateTime, nullable=False, server_default=sqlfunc.now(),
        onupdate=datetime.utcnow)


class TrackCreations:
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


class Location(db.Model, TrackCreations, TrackUpdates):
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


class LocationMember(db.Model, TrackCreations):
    __tablename__ = 'location_access'

    location_id = Column(ForeignKey('location.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    __table_args__ = (PrimaryKeyConstraint(location_id, user_id),)

    def to_dict(self):
        return {
            'location_id': self.location_id,
            'user_id': self.user_id
        }


class Item(db.Model, TrackCreations, TrackUpdates):
    __tablename__ = 'item'
    id = Id()
    name = Column(String(256), nullable=False)
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
    __tablename__ = 'item_stock'

    item_id = Column(ForeignKey('item.id'), nullable=False)
    location_id = Column(ForeignKey('location.id'), nullable=False)
    __tableargs__ = (PrimaryKeyConstraint(item_id, location_id),)
    # Quantity for now is in milligrams. Will add enum later...
    quantity = Column(Integer, nullable=False)
    # Price of an item stock will be coalesced from the item.
    price = Column(Numeric(15, 2))


def drop_all():
    db.drop_all()


def create_all():
    db.create_all()
