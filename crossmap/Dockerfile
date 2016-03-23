FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    build-essential \
    python \
    python-dev \
    python-pip \
    wget \
    zlib1g-dev

RUN sudo pip install \
    Cython \
    numpy

RUN wget -O /tmp/CrossMap-0.2.1.tar.gz http://downloads.sourceforge.net/project/crossmap/CrossMap-0.2.1.tar.gz && \
    cd /tmp && tar xvfz CrossMap-0.2.1.tar.gz && \
    cd /tmp/CrossMap-0.2.1 && \
    python setup.py install && \
    rm -rvf /tmp/*

RUN mkdir /opt/crossmap
COPY wrapper.sh /opt/crossmap/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/crossmap/wrapper.sh"]
