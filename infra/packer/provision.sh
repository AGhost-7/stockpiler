#!/usr/bin/env bash

set -e

sudo apt-get update

# {{{ ansible requirements
sudo apt-get install python python-pip -y
sudo python -m pip install certifi docker-py
# }}}

# {{{ default firewall settings
sudo apt-get install ufw -y
sudo ufw reset
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw enable
# }}}

# {{{ install docker

# required for the virtualbox image.
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add --
echo 'deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable' | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install docker-ce -y
# }}

