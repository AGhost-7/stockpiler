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
