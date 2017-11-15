
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

CMD ["twistd", "-ny", "buildbot.tac"]
