#!/usr/bin/env bash

ansible-playbook -i "$1" -e "docker_image_tag=$2" deploy.yml
