from datetime import datetime
from uuid import UUID

from flask import abort, jsonify
from webargs.flaskparser import use_args

from marshmallow import Schema, fields

from service.server import app
from service.models import Address, AddressEvent, User

# You can user this logger by calling logger.info()
logger = app.logger


###### Helper Functions ######

def get_address(user_id: UUID, payload: dict) -> Address:
    return Address(
        user_id=user_id,
        street_one=payload.get("street_one"),
        street_two=payload.get("street_two"),
        city=payload.get("city"),
        state=payload.get("state"),
        zip_code=payload.get("zip_code"),
    )


def get_address_event(address: Address, event_type: str) -> AddressEvent:
    return AddressEvent(
        address_id=address.id,
        user_id=address.user_id,
        event_type=event_type,
        created=datetime.utcnow(),
        street_one=address.street_one,
        street_two=address.street_two,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
    )


###### Query Schemas ######

class GetAddressQueryArgsSchema(Schema):
    date = fields.Date(required=False, missing=datetime.utcnow().date())


###### Validation and Response Schemas ######

class AddressRequestSchema(Schema):
    class Meta:
        ordered = True

    street_one = fields.Str(required=True, max=128)
    street_two = fields.Str(required=False, max=128)
    city = fields.Str(required=True, max=128)
    state = fields.Str(required=True, max=2)
    zip_code = fields.Str(required=True, max=10)


class AddressResponseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.UUID(required=True)

    street_one = fields.Str(required=True, max=128)
    street_two = fields.Str(required=False, max=128)
    city = fields.Str(required=True, max=128)
    state = fields.Str(required=True, max=2)
    zip_code = fields.Str(required=True, max=10)


class AddressEventSchema(Schema):
    class Meta:
        ordered = True

    id = fields.UUID(required=True)

    created = fields.DateTime(required=True, timezone=True)
    event_type = fields.Str(required=True, max=128)

    street_one = fields.Str(required=True, max=128)
    street_two = fields.Str(required=False, max=128)
    city = fields.Str(required=True, max=128)
    state = fields.Str(required=True, max=2)
    zip_code = fields.Str(required=True, max=10)


###### Address Endpoints ######

@app.route("/users/<uuid:user_id>/addresses", methods=["GET"])
@use_args(GetAddressQueryArgsSchema(), location="querystring")
def get_addresses(args: dict, user_id: UUID):
    user = User.query.get(user_id)

    if user is None:
        abort(404, description="user does not exist")

    addresses = Address.query.filter_by(user_id=user_id).all()

    if len(addresses) == 0:
        abort(404, description="user does not have an address, please create one")

    return jsonify(AddressResponseSchema(many=True).dump(addresses))


@app.route("/users/<uuid:user_id>/addresses", methods=["POST"])
@use_args(AddressRequestSchema())
def create_address(payload: dict, address_id: UUID):
    address = get_address(user_id, payload)
    address_event = get_address_event(address, 'address_created')
    
    db.session.add(address)
    db.session.add(address_event)
    db.session.commit()
    db.session.refresh(address)

    return jsonify(AddressResponseSchema().dump(address))


@app.route("/addresses/<uuid:address_id>", methods=["PUT"])
@use_args(AddressRequestSchema())
def update_address(payload: dict, address_id: UUID):
    address = Address.query.get(address_id)

    if address is None:
        abort(404, description="address does not exist")

    new_address = get_address(user_id, payload)
    address_event = get_address_event(new_address, 'address_updated')

    db.session.add(address)
    db.session.add(address_event)
    db.session.commit()
    db.session.refresh(address)

    return jsonify(AddressResponseSchema().dump(address))


###### Address Event Endpoints ######
@app.route("/addresses/<uuid:address_id>/address_events", methods=["GET"])
def get_address_events(address_id: UUID):
    address = Address.query.get(address_id)

    if address is None:
        abort(404, description="address does not exist")

    address_events = AddressEvent.query.filter_by(address_id=address_id).all()

    return jsonify(AddressEventSchema(many=True).dump(address_events))
