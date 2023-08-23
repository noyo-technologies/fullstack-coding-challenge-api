
# Table of Contents
- [TLDR;](#tldr)
- [Setup](#setup)
- [Endpoints](#endpoints)
  - [User endpoints](#user-endpoints)
  - [Address endpoints](#address-endpoints)

## TLDR
This is the back-end python component to our full-stack coding challenge. It is a service that supports
some basic create/update endpoints for Users and their Addresses. It also implicitly creates AddressEvents 
when an Address is created or updated.

You should familiarize yourself with this code, particularly the address endpoints in `/api/addresses.py`.

**Please refer to the [UI repository](https://github.com/noyo-technologies/fullstack-coding-challenge-ui) for the remainder of the challenge instructions.**


## Setup
For many repositories at Noyo, we use common setup scripts to easily get your local environment started.
In order to build the local docker containers, you'll just need to run `./go build` from the command line.
For seeding test data, you can run `/.go seed`. 

The full list of supported commands are below, or you can simply run `./go` to see these in the command line.
```
build            Build the local containers
start            Start up the docker containers
stop             Stop the docker containers
seed             Seed the database. Note - This will delete existing data when run.
test             Run the full test suite. Note - This will delete existing data when run.
nuke             Stop all containers and remove volumes
```

Once the containers are running, you should be able to access the API at `http://localhost:5050`. With data seeded,
you should be able to see it at `http://localhost:5050/users`

## Endpoints
### User Endpoints
- `GET http://localhost:5050/users` - List all users
- `GET http://localhost:5050/user/:id` - Get user by ID
- `POST http://localhost:5050/users` - Create user
- `PATCH http://localhost:5050/users` - Update user

### Address Endpoints
- `GET http://localhost:5050/users/:id/addresses` - List all addresses for a user
- `POST http://localhost:5050/users/:id/addresses` - Create address for a user
- `GET http://localhost:5050/addresses/:id/address_events` - List all address events for an address
- `PUT http://localhost:5050/addresses/:id` - Update address

