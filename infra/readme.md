# Infrastructure
Stuff for the code to run in prod, etc. WIP

## Developing
- Build the packer image (see instructions in `packer` directory).
- Add the generated image: `vagrant box add stockpiler-ubuntu-16.04-amd64 packer/stockpiler-ubuntu-16.04-amd64.box`
- run `vagrant up`.

## Ramblings...
- avoid unreproducible machine state:
	- build packer images.
	- use docker containers.
- share configs:
	- build images for vagrant and prod from the same configs/scripts.
	- use the same compose file for running ci and testing locally.
- Terraform+ansible?

## Topology

### Initial
Goal for this is to have an initial PoC setup.

- web:
	- certbot
	- front1 (blue)
	- front2 (green)
	- api1 (blue)
	- api2 (green)
	- load balancer
- database
- ci:
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
