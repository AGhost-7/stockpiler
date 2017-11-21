FROM python:3.5.2

WORKDIR /bender

COPY ./requirements.txt /bender/requirements.txt

RUN pip install -r requirements.txt

COPY ./bender.py /bender/bender.py

CMD ["./bender.py"]
