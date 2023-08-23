from datetime import datetime, timedelta
from uuid import uuid4

from service.server import app
from faker import Faker
from service.server import db

from service.models import (
    Address,
    AddressEvent,
    User,
)

with app.app_context():
    print()
    print('Removing existing database entries...')
    model_class_list = [AddressEvent, Address, User]

    for model in model_class_list:
        db.session.query(model).delete()
        db.session.commit()

    fake = Faker()
    users = []
    for _ in range(5):
        users.append(
            User(
                id=uuid4(),
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
            )
        )

    print('Seeding new data...')
    addresses = []
    address_events = []
    for user in users:
        state = fake.state_abbr(include_territories=False)
        address = Address(
            id=uuid4(),
            user_id=user.id,
            street_one=fake.street_address(),
            street_two=None,
            city=fake.city(),
            state=state,
            zip_code=fake.postalcode_in_state(state),
        )

        # Add creation event, as of 15 minutes ago
        # This will have the address of 123 Fake Street, in the same city and zip
        address_created_event = AddressEvent(
            id=uuid4(),
            address_id=address.id,
            user_id=user.id,
            event_type='address_created',
            created=datetime.utcnow() - timedelta(minutes=15),
            street_one='123 Fake Street',
            street_two=None,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
        )

        # Add modified event, now
        address_modified_event = AddressEvent(
            id=uuid4(),
            address_id=address.id,
            user_id=user.id,
            event_type='address_updated',
            created=datetime.utcnow(),
            street_one=address.street_one,
            street_two=address.street_two,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
        )

        addresses.append(address)
        address_events.append(address_created_event)
        address_events.append(address_modified_event)

    db.session.add_all(users)
    db.session.add_all(addresses)
    db.session.add_all(address_events)
    db.session.commit()

    print('Done!')
