from uuid import UUID
from flask import abort, jsonify
from webargs.flaskparser import use_args
from marshmallow import Schema, fields

from service.server import app, db
from service.models import User


###### Validation Schemas ######
class UpdateOrFindUserSchema(Schema):
    first_name = fields.Str(max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(max=128)


class CreateUserSchema(Schema):
    first_name = fields.Str(required=True, max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(required=True, max=128)


###### Response Schemas ######
class UserResponseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.UUID(required=True)

    first_name = fields.Str(required=True, max=128)
    middle_name = fields.Str(max=128)
    last_name = fields.Str(required=True, max=128)


@app.route("/users", methods=["GET"])
@use_args(UpdateOrFindUserSchema(), location="query")
def get_users(args: dict):
    users = User.query.filter_by(**args).order_by(User.last_name.asc()).all()
    return jsonify(UserResponseSchema(many=True).dump(users))


@app.route("/users/<uuid:id>", methods=["GET"])
def get_user(id: UUID):
    # Check if a user exists and abort 404 if not found
    user = User.query.get(id)
    if user is None:
        abort(404, description="user does not exist")

    return jsonify(UserResponseSchema().dump(user))


@app.route("/users", methods=["POST"])
@use_args(CreateUserSchema())
def create_user(payload: dict):
    user = User(
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
        middle_name=payload.get("middle_name"),
    )

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(UserResponseSchema().dump(user))


@app.route("/users/<uuid:id>", methods=["PATCH"])
@use_args(UpdateOrFindUserSchema())
def update_user(payload: dict, id: UUID):
    # Check if a user exists and abort 404 if not found
    user = db.session.query(User).get(id)
    if user is None:
        abort(404, description="user does not exist")

    # loop over items and set attributes
    for update_key, update_value in payload.items():
        setattr(user, update_key, update_value)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(UserResponseSchema().dump(user))
