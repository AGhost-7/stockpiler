#!/usr/bin/env bash

# script used to run tests in docker

set -e

flake8 {test,api,bin}
api_create_tables
api &
pid=$?
trap "kill $pid" EXIT
pytest --exitfirst test/*.py
