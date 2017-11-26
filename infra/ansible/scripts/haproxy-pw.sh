#!/usr/bin/env bash

# Used to randomly generate the passwords for securing staging.

set -e

if ! command -v mkpasswd; then
	sudo apt-get update
	# for some reason mkpasswd is available in this package???
	sudo apt-get install whois -y
fi

plain="$(openssl rand -hex 20)"
hash="$(mkpasswd -m sha-512 "$plain")"

echo "Generated plain text password: $plain"
echo "Hashed password: $hash"
