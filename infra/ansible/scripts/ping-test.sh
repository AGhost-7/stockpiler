#!/usr/bin/env bash

ansible -m ping \
	--inventory=$PWD/test/vagrant_inventory \
	--private-key=$PWD/test/vagrant_key \
	all
