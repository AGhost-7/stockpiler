
# Built from scratch to use python 3. The dead process handling in the official
# image also isn't necessary since we're going to be running every build in
# a fresh container. This is why the image is simpler as well.

FROM python:3.5.2

# Install buildbot worker a twisted requirement
RUN pip install buildbot-worker twisted[tls]

# Copy buildbot's twistd "entrypoint"
COPY ./buildbot.tac /buildbot/buildbot.tac

# Dependencies for the test script
COPY ./requirements.txt /buidlbot/requirements.txt

RUN pip install --upgrade -r /buidlbot/requirements.txt

# Container spawn script and test runner.
COPY ./test.py /buildbot/test.py

WORKDIR /buildbot

ENV DOCKER_CLI_SHA256 "7dcd87ba776743b3cdf584fb54b85318ac4e4671e1c1afc24e24697f9e101a2d" 

# Download only the docker client as the host already has the daemon.
RUN apt-get update && \
	apt-get install -y curl debsums && \
	curl -o /tmp/docker.tgz https://download.docker.com/linux/static/stable/x86_64/docker-17.09.0-ce.tgz && \
	tar xvf /tmp/docker.tgz -C /tmp && \
	mv /tmp/docker/docker /usr/local/bin/docker && \
	rm -rf /tmp/docker* && \
	[ "$(sha256sum /usr/local/bin/docker | awk '{print $1}')" = "$DOCKER_CLI_SHA256" ] && \
	apt-get remove -y curl debsums && \
	rm -rf /var/lib/apt/lists/*

CMD ["twistd", "-ny", "buildbot.tac"]
