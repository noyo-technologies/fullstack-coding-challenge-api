import uuid
from service.models import User

from service.server import db
from faker import Faker

fake = Faker()


def test_create_user_with_validation_error(test_context, client):
    with test_context:
        create_response = client.post("/users", json={})

        assert create_response.status_code == 422
        assert create_response.json == {
            "errors": {
                "json": {
                    "first_name": ["Missing data for required field."],
                    "last_name": ["Missing data for required field."],
                }
            }
        }


def test_create_user_success(test_context, client):
    with test_context:
        create_response = client.post(
            "/users",
            json={"first_name": "John", "middle_name": "J", "last_name": "Doe"},
        )

        assert create_response.status_code == 200
        assert create_response.json["first_name"] == "John"
        assert create_response.json["middle_name"] == "J"
        assert create_response.json["last_name"] == "Doe"


def test_get_user_not_found(test_context, client):
    with test_context:
        get_response = client.get(f"/users/{uuid.uuid4()}")

        assert get_response.status_code == 404
        assert get_response.json == {"error": "user does not exist"}


def test_get_user_success(test_context, client):


    with test_context:
        user = User(first_name="John", last_name="Doe")

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        get_response = client.get(f"/users/{user.id}")

        assert get_response.status_code == 200
        assert get_response.json == {
            "id": str(user.id),
            "first_name": "John",
            "middle_name": None,
            "last_name": "Doe",
        }


def test_get_users_success(test_context, client):
    with test_context:
        user_one = User(first_name="John", last_name="Doe")
        user_two = User(first_name="Jane", last_name="Doe")

        db.session.add(user_one)
        db.session.add(user_two)
        db.session.commit()
        
        get_response = client.get("/users")

        assert get_response.status_code == 200
        assert len(get_response.json) == 2


def test_patch_user_with_validation_error(test_context, client):
    with test_context:
        user = User(first_name="John", last_name="Doe")

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        patch_response = client.patch(
            f"/users/{user.id}", json={"first_name": None, "last_name": None}
        )

        assert patch_response.status_code == 422
        assert patch_response.json == {
            "errors": {
                "json": {
                    "first_name": ["Field may not be null."],
                    "last_name": ["Field may not be null."],
                }
            }
        }


def test_patch_user_user_does_not_exist(test_context, client):
    with test_context:
        user = User(first_name="John", last_name="Doe")

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)


        patch_response = client.patch(
            f"/users/{uuid.uuid4()}", json={"first_name": "Jane"}
        )

        assert patch_response.status_code == 404
        assert patch_response.json == {"error": "user does not exist"}


def test_patch_user_success(test_context, client):
    with test_context:
        user = User(first_name="John", last_name="Doe")

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        patch_response = client.patch(
            f"/users/{user.id}",
            json={"last_name": "Smith"},
        )

        assert patch_response.status_code == 200
        assert patch_response.json == {
            "id": str(user.id),
            "first_name": "John",
            "middle_name": None,
            "last_name": "Smith",
        }
