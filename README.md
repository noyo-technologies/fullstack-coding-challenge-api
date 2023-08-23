
# Table of Contents
- [TLDR;](#tldr)
- [Setup](#setup)

## TLDR
This is the back-end python component to our full-stack coding challenge. It is a service that supports
some basic create/update endpoints for Users and their Addresses. It also implicitly creates AddressEvents 
when an Address is created or updated.

You should familiarize yourself with this code, particularly the address endpoints in `/api/addresses.py`.

Please refer to the [UI repository](https://github.com/noyo-technologies/fullstack-coding-challenge-api) for the remainder of the challenge instructions.


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

