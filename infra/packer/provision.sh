#!/usr/bin/env bash

# Defines a basic vm use for all servers.

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
# allow only private addresses to access ssh by default.
sudo ufw allow from 192.168.0.0/16 to any port ssh
sudo ufw allow from 10.0.0.0/8 to any port ssh
sudo ufw allow from 172.16.0.0/12 to any port ssh
sudo ufw --force enable

# }}}

# {{{ misc utils

# For dig, etc.
sudo apt-get install -y --no-install-recommends dnsutils

# Needed for netstat, etc.
sudo apt-get install -y --no-install-recommends net-tools

# Packet sniffer for debugging.
sudo apt-get install -y --no-install-recommends tcpflow

# Very usefull for finding issues coming from syscalls
sudo apt-get install -y --no-install-recommends strace

# a better top
sudo apt-get install -y --no-install-recommends htop

# editing tool
sudo apt-get install -y --no-install-recommends vim

# terminal multiplexing
sudo apt-get install -y --no-install-recommends tmux

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
sudo apt-get install docker-ce=17.09.0~ce-0~ubuntu -y
sudo systemctl enable docker

# }}

