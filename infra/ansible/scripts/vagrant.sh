#!/usr/bin/env bash

# source this script to load up the appropriate parameters

alias ansible-playbook='ansible-playbook \
	--inventory=test/vagrant_inventory \
	--private-key=test/vagrant_key'

