FROM ubuntu:12.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y libhdf5-serial-dev \
    python-software-properties

RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install -y libstdc++6-4.7-dev

RUN ln -s /usr/lib/libhdf5.so /usr/lib/libhdf5.so.7

COPY kallisto /usr/local/bin/

RUN mkdir /opt/kallisto/
COPY wrapper.sh /opt/kallisto/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/kallisto/wrapper.sh"]