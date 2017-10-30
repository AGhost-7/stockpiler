#!/usr/bin/env bash
openssl req \
  -newkey rsa:4096 -nodes -sha256 -keyout test/registry.key \
  -x509 -days 365 -out test/registry.crt
