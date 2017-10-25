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
	git clone --depth=3 --branch "$GIT_REV" git@github.com:AGhost-7/stockpiler && \
	cd /stockpiler/api && \
	pip install .

FROM python:3.5.2

COPY --from=0 /env /env

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["api"]
