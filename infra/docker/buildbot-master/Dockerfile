FROM buildbot/buildbot-master:master

RUN apk update && \
	apk add openssh-client

COPY ./master.cfg /var/lib/buildbot/master.cfg
