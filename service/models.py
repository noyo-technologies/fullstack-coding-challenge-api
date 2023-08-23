import uuid

from sqlalchemy.dialects.postgresql import UUID

from service.server import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    first_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=False)

    # sql alchemy will populate this attribute as a list
    # of all addresses that have Address.user_id == User.id
    addresses = db.relationship("Address")


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    street_one = db.Column(db.String(128), nullable=False)
    street_two = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    address_events = db.relationship("AddressEvent")


class AddressEvent(db.Model):
    __tablename__ = "address_events"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())

    created = db.Column(db.DateTime(timezone=True), nullable=False)
    event_type = db.Column(db.String(128), nullable=False)

    address_id = db.Column(UUID(as_uuid=True), db.ForeignKey("addresses.id"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    street_one = db.Column(db.String(128), nullable=False)
    street_two = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
