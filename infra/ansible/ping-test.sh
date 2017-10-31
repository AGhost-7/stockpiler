#!/usr/bin/env bash

ansible -m ping \
	--inventory=test/vagrant_inventory \
	--private-key=test/vagrant_key \
	all
