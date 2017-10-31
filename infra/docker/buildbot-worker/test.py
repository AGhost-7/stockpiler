#!/usr/bin/env python3

# Test runner which spins up docker containers based on the contents of the
# current branch.

import docker
from uuid import uuid4
from glob import glob
from os import path
import logging
import yaml
import sys
import json
import time


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)

client = docker.APIClient(base_url='unix://var/run/docker.sock')

build_id = str(uuid4())
network_name = 'buildbot-' + build_id


class ComposeService:

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.container_id = None

    def up(self):
        logging.info('Bringing up service %s', self.name)
        endpoint_config = client.create_endpoint_config(
            aliases=[self.name]
        )
        network_config = client.create_networking_config({
            network_name: endpoint_config
        })
        response = client.create_container(
            image=self.config['image'],
            command=self.config.get('command'),
            networking_config=network_config,
            environment=self.config.get('environment'))
        self.container_id = response['Id']
        client.start(container=self.container_id)

    def down(self):
        if self.container_id is not None:
            logging.info('Taking down service %s', self.name)
            client.stop(container=self.container_id)
            client.remove_container(container=self.container_id)


class TestGroup:

    def __init__(self, dockerfile):
        self.dockerfile = dockerfile
        self.directory = path.dirname(self.dockerfile)
        self.name = path.basename(self.directory)
        self.image_name = 'buildbot_worker_' + self.name
        self.image_id = None
        self.container_id = None
        self.services = []

    def parse_services(self, compose_file):
        with open(compose_file) as ref:
            config = yaml.load(ref)
            for name, service_config in config['services'].items():
                self.services.append(ComposeService(name, service_config))

    def build(self):
        logging.info(
            'Building image %s from file %s', self.image_name, self.dockerfile)
        response = client.build(
            path=self.directory,
            dockerfile='Dockerfile.test',
            tag=self.image_name)

        for chunk in response:
            parsed_chunk = json.loads(chunk.decode('utf8'))
            if 'stream' in parsed_chunk:
                sys.stdout.write(parsed_chunk['stream'])
            elif 'aux' in parsed_chunk:
                self.image_id = parsed_chunk['aux']['ID']

    def run_tests(self):
        logging.info('Waiting for containers to boot up')
        time.sleep(10)
        network_config = client.create_networking_config({
            network_name: client.create_endpoint_config()
        })
        response = client.create_container(
            image=self.image_id,
            networking_config=network_config)
        self.container_id = response['Id']
        client.start(container=self.container_id)
        logging.info('Testing container started')
        response = client.attach(
            self.container_id, stream=True, stdout=True, stderr=True)
        for res in response:
            sys.stdout.write(res.decode('utf8'))

        response = client.inspect_container(self.container_id)
        return response['State']['ExitCode']

    def clean_tests(self):
        if self.container_id is not None:
            logging.info('Removing testing container')
            client.stop(container=self.container_id)
            client.remove_container(container=self.container_id)

    def spawn_services(self):
        compose_file = path.join(self.directory, 'docker-compose.yml')
        if path.exists(compose_file):
            logging.info(
                'Compose file found at %s, bringing up services', compose_file)
            self.parse_services(compose_file)
            for service in self.services:
                service.up()
        else:
            logging.info(
                'Could not found compose file at %s... no services to run')

    def teardown_services(self):
        for service in self.services:
            try:
                service.down()
            except Exception:
                logging.error('Failed to bring down service %s', service.name)


try:
    test_groups = []
    client.create_network(network_name)
    exit_code = 0
    for dockerfile in glob('./*/Dockerfile.test'):
        test_group = TestGroup(dockerfile)
        test_group.build()
        test_groups.append(test_group)

    for test_group in test_groups:
        logging.info('Running test group %s', test_group.name)
        test_group.spawn_services()
        exit_code = test_group.run_tests()
        if exit_code > 0:
            raise Exception('Test returned exit code %s' % exit_code)

finally:
    for test_group in test_groups:
        test_group.teardown_services()
        test_group.clean_tests()

    logging.info('Deleting network')
    client.remove_network(network_name)
