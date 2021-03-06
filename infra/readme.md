# Infrastructure
Stuff for the code to run in prod, etc. WIP

## Developing

### Install vagrant
```
sudo apt-get install vagrant -y
```

### Get the base image
Build the packer image (see instructions in `packer` directory), then add the
generated image:
```
vagrant box add stockpiler-ubuntu-16.04-amd64 packer/stockpiler-ubuntu-16.04-amd64.box
```

### Boot up
Just...
```
vagrant up
```

### Configure Github Integrations
You will need to specify the following variables in `ansible/group_vars/all`
for the buildbot server to work correctly:
```yaml
buildbot_github_api_token: ''
buildbot_oauth_id: ''
buildbot_oauth_secret: ''
buildbot_github_webhook_secret: ''
```

### Bring up the system
Login:
```
vagrant ssh
cd /vagrant/ansible
```

Ping your servers to check that everything is in place:
```
ansible -m ping -i test/vagrant_inventory all
```

Run the main playbook:
```
ansible-playbook -i test/vagrant_inventory site.yml
```

## Topology

### Initial
Goal for this is to have an initial PoC setup.

- web:
	- certbot
	- ui1
	- ui2
	- api1
	- api2
	- load balancer
- database
- build:
	- buildbot master
	- buildbot slave
	- registry
- orchestration:
	- ansible
	- terraform (maybe)

total: 4 servers.

### Final
Will be used for the completed production environment. Will comprise of a zero
downtime setup (blue/green deployment) with high availability.

- load balancer1 & certbot
- load balancer2 & certbot (standby - floating ip failover)
- api1 (blue)
- api2 (blue)
- api3 (green)
- api4 (green)
- front1 (blue)
- front2 (blue)
- front3 (green)
- front4 (green)
- db master
- db master (standby - failover? maxscale?)
- orchestrator
- registry
- buildbot master/slave
 
total: 15 servers.

resources:
https://www.digitalocean.com/community/tutorials/how-to-create-a-high-availability-setup-with-corosync-pacemaker-and-floating-ips-on-ubuntu-14-04
https://mariadb.com/resources/blog/mariadb-maxscale-high-availability-active-standby-cluster
