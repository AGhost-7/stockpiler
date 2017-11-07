#!/usr/bin/env bash

set -e

for livedir in /etc/letsencrypt/live/*; do
	domain="$(basename "$livedir")"
	cat "$livedir"/{fullchain.pem,privkey.pem} > /etc/haproxy/certs/"$domain"
done

docker kill --signal=USR2 haproxy
