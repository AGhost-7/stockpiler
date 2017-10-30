#!/usr/bin/env bash

ansible-playbook \
	--inventory=test/vagrant_inventory \
	--private-key=test/vagrant_key \
	"$@"

