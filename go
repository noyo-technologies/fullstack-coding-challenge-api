#!/bin/bash

set -e

DC="docker-compose"

function helptext {
    echo "Usage: ./go <command>"
    echo ""
    echo "Available commands are:"
    echo "    build            Build the local containers"
    echo "    start            Start up the docker containers"
    echo "    stop             Stop the docker containers"
    echo "    seed             Seed the database. Note - This will delete existing data when run."
    echo "    test             Run the full test suite. Note - This will delete existing data when run."
    echo "    nuke             Stop all containers and remove volumes"
}

function build {
  ${DC} build
}

function seed {
  ${DC} exec service python seed.py
}

function start {
  ${DC} up -d
}

function stop {
  ${DC} down
}

function test {
  ${DC} exec service pytest .
}

function nuke {
  ${DC} down --remove-orphans --volumes
}

case "$1" in
  build)  build ;;
  start)  start ;;
  stop)   stop  ;;
  seed)   seed  ;;
  test)   test  ;;
  nuke)   nuke  ;;
  *)      helptext; exit 1 ;;
esac

