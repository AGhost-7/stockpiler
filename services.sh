#!/usr/bin/env bash

# Sortcut for bringing up the entire app for development. This
# script is also used by the build server.
#
# usage:
# PROJECT_DIR=yourhostdir ./services.sh up
# PROJECT_DIR=yourhostdir ./services.sh down

docker-compose $(echo */docker-compose.yml | sed 's/^/ -f /') "$@"
