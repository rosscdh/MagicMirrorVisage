FROM python:3.6-slim

RUN apt-get -y update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    libopencv-dev python-opencv \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*


# Install DLIB
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.8' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no USE_SSE4_INSTRUCTIONS

WORKDIR /usr/share/app

# Copy web service script
ADD . /usr/share/app

WORKDIR /usr/share/app/face_recognition
RUN pip3 install -r requirements.txt && python3 setup.py install

WORKDIR /usr/share/app
RUN pip3 install -r /usr/share/app/requirements.txt

# Start the web service
#CMD cd /root/ && \
#    python3 facerec_service.py
