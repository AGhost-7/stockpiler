#!/usr/bin/env bash

# Deploy script used by the CI/CD server. The server is only permitted to
# run specific commands on the orchestration machine. By following the
# principle of least privilege we are preventing an attacker from gaining
# access to production data if the CI/CD server is ever compromised.

inventory="$1"
tag="$2"
env="$3"

if [ -z "$tag" ]; then
	tag="latest"
fi

if [ -z "$env" ]; then
	env="stage"
fi

# TODO: This still allows variable injection attacks. Would want to protect
# against this in case the CI/CD server would be compromised.
ansible-playbook -i "$inventory" -e "docker_image_tag=$tag" --limit "$env" deploy.yml
