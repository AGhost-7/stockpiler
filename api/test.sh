#!/usr/bin/env bash

# script used to run tests in docker

set -e

api_create_tables
api &
pid=$?
trap "kill $pid" EXIT
pytest --exitfirst test/*.py
