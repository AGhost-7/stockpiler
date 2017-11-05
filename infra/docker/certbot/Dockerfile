FROM debian:jessie

# {{{ install tini for collecting zombie processes
ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /sbin/tini
RUN chmod +x /sbin/tini
ENTRYPOINT ["/sbin/tini", "--"]
# }}}

# {{{ install cron job runner
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.4/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=3a631023f9f9dd155cfa0d1bb517a063d375055a

RUN apt-get update && \
	apt-get install curl -y && \
	curl -fsSLO "$SUPERCRONIC_URL"  && \
	echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - && \
	chmod +x "$SUPERCRONIC" && \
	mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" && \
	ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic && \
	apt-get remove curl -y && \
	rm -rf /var/lib/apt/lists/*
# }}}

# {{{ install certbot
RUN	echo 'deb http://ftp.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/backports.list && \
	apt-get update && \
	apt-get install -y certbot -t jessie-backports

COPY ./concat-certs.sh /concat-certs.sh
# }}}

VOLUME ["/etc/letsencrypt/live"]

CMD ["supercronic", "/etc/crontab"]
