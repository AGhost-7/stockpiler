#!/usr/bin/env bash

set -e

for directory in /etc/letsencrypt/live/*; do
	cat "$directory"/{fullchain.pem,privkey.pem} > "$directory"/haproxy.pem
done

