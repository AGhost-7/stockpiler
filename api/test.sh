#!/usr/bin/env bash

set -e

api_create_tables
api &
pid=$?
trap "kill $pid" EXIT
pytest test/*.py
