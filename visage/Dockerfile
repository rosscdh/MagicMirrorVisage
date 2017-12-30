FROM python:3.6-slim

RUN apt-get -y update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake \
    httpie \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

ADD . /usr/local/app

WORKDIR /usr/local/app

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/gunicorn", "app:api", "-w", "2", "-b", "0.0.0.0:8080", "--reload"]