#!/usr/bin/env bash

output_dir="$PWD/test"

# Used by docker registry
#openssl req \
#  -newkey rsa:4096 -nodes -sha256 -keyout "$output_dir/registry.key" \
#  -x509 -days 365 -out "$output_dir/registry.crt"

# used for the domain
domain='stockpiler.ca'
openssl req \
       -newkey rsa:2048 -nodes -keyout "$output_dir/$domain.key" \
       -x509 -days 365 -out "$output_dir/$domain.crt"

