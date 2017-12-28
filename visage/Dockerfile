FROM python:3-alpine

RUN apk --update add build-base jpeg-dev zlib-dev

ADD . /usr/local/app

WORKDIR /usr/local/app

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/gunicorn", "app:api", "-w", "2", "-b", "0.0.0.0:8080", "--reload"]