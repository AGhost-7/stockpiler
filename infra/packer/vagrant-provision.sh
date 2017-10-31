#!/usr/bin/env bash

# Additional provisioning specifically for vagrant

set -e

sudo mount -o loop,ro ~/VBoxGuestAdditions.iso /mnt/
sudo /mnt/VBoxLinuxAdditions.run || :
sudo umount /mnt/
rm -f ~/VBoxGuestAdditions.iso

mkdir -p ~/.ssh
curl -fsSLo ~/.ssh/authorized_keys https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub
chmod 700 ~/.ssh/
chmod 600 ~/.ssh/authorized_keys

sudo usermod -aG docker vagrant

# this is the port vagrant uses to ssh
sudo ufw allow 2222
