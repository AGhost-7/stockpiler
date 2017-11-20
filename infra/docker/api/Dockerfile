FROM python:3.5.2

ARG GIT_REV

ARG SSH_KEY

RUN pip install virtualenv && \
	virtualenv /env

RUN mkdir -p ~/.ssh && \
	echo "$SSH_KEY" > ~/.ssh/id_rsa && \
	chmod 400 ~/.ssh/id_rsa && \
	ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN . /env/bin/activate && \
	git clone git@github.com:AGhost-7/stockpiler && \
	cd /stockpiler && \
	git reset --hard "$GIT_REV" && \
	cd api && \
	pip install -r requirements.txt && \
	pip install .

FROM python:3.5.2

COPY --from=0 /env /env

COPY ./entrypoint.sh /entrypoint.sh

ENV MAIL_SERVER=smtp.mailgun.org

ENV MAIL_PORT=25

ENV MAIL_USE_TLS=true

ENTRYPOINT ["/entrypoint.sh"]

CMD ["api"]
