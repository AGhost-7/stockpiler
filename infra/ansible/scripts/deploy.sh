#!/usr/bin/env bash

inventory="$1"
tag="$2"
env="$3"

if [ -z "$tag" ]; then
	tag="latest"
fi

if [ -z "$env" ]; then
	env="stage"
fi

ansible-playbook -i "$inventory" -e "docker_image_tag=$tag" --limit "$env" deploy.yml
