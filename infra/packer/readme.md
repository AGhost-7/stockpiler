# Packer Image: VM base
Packer configuration for Digital Ocean droplet for use with docker and ansible.

Tested using packer version 1.1.1.

## How to use
Log into your digital ocean account, create an api token from the settings and
run the following to build the VM image:
```
packer build -var 'api_token=YOUR API TOKEN' template.json
```

After building the image you will see it pop up in the snapshots tab when creating a droplet.

### Building only for vagrant
```
packer build -var 'api_token=YOUR API TOKEN' -only vagrant template.json
```
