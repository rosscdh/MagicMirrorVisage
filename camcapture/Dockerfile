FROM python:3.6-slim
MAINTAINER Josip Janzic <josip.janzic@gmail.com>

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libopencv-dev

RUN pip install numpy

WORKDIR /usr/share/app

# Copy web service script
ADD . /usr/share/app

WORKDIR /usr/share/app
RUN pip3 install -r /usr/share/app/requirements.txt

# Start the web service
#CMD cd /root/ && \
#    python3 facerec_service.py
