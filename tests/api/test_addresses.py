import pytest
import uuid

from datetime import date, timedelta

from service.models import Address, User

from service.server import db
from flask.testing import FlaskClient
from flask.ctx import AppContext


@pytest.fixture
def seed_user(test_context: AppContext):
    with  test_context:
        """seed and return a user"""
        user = User(first_name="John", last_name="Doe")

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        yield user


@pytest.fixture
def seed_user_and_address(seed_user: User):
    """seed a user (via the seed_user fixture) and a seed a single address"""
    address = Address(
        user_id=seed_user.id,
        street_one="123 Market St",
        street_two=None,
        city="San Francisco",
        state="CA",
        zip_code="94613",
    )
    db.session.add(address)
    db.session.commit()
    db.session.refresh(address)

    yield address


def test_create_address_with_validation_error(
    test_context: AppContext, client: FlaskClient, seed_user: User
):
    with test_context:
        response = client.post(f"/users/{seed_user.id}/addresses", json={})

        assert response.status_code == 422
        assert response.json == {
            "errors": {
                "json": {
                    "city": ["Missing data for required field."],
                    "state": ["Missing data for required field."],
                    "street_one": ["Missing data for required field."],
                    "zip_code": ["Missing data for required field."],
                }
            }
        }


def test_get_address(
    test_context: AppContext, client: FlaskClient, seed_user_and_address: Address
):
    with test_context:
        response = client.get(
            f"/users/{seed_user_and_address.user_id}/addresses"
        )
        assert response.status_code == 200


def test_get_address_no_user(test_context: AppContext, client: FlaskClient):
    with test_context:
        response = client.get(f"/users/{uuid.uuid4()}/addresses")
        assert response.status_code == 404
        assert response.json == {"error": "user does not exist"}


def test_get_address_no_address_exists(
    test_context: AppContext, client: FlaskClient, seed_user: User
):
    with test_context:
        response = client.get(f"/users/{seed_user.id}/addresses")
        assert response.status_code == 404
        assert response.json == {
            "error": "user does not have an address, please create one"
        }
