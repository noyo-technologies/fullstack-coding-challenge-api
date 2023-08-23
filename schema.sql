CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),

    first_name VARCHAR(128) NOT NULL,
    middle_name VARCHAR(128),
    last_name VARCHAR(128) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS addresses (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL REFERENCES users,
    street_one VARCHAR(128) NOT NULL,
    street_two VARCHAR(128),
    city VARCHAR(128) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS address_events (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),

    created TIMESTAMP WITH TIME ZONE NOT NULL,
    event_type VARCHAR(128) NOT NULL,

    address_id UUID NOT NULL REFERENCES addresses,
    user_id UUID NOT NULL REFERENCES users,

    street_one VARCHAR(128) NOT NULL,
    street_two VARCHAR(128),
    city VARCHAR(128) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (id)
);
