FROM buildbot/buildbot-master:master

RUN apk add --no-cache openssh-client

RUN apk add --no-cache musl-dev gcc python-dev && \
	pip install treq txrequests && \
	apk del --no-cache musl-dev gcc python-dev

COPY ./master.cfg /var/lib/buildbot/master.cfg
