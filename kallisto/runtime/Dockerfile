FROM ubuntu:12.04

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update && apt-get install -y libhdf5-dev

COPY kallisto /usr/local/bin/

RUN mkdir /opt/kallisto/
COPY wrapper.sh /opt/kallisto/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/kallisto/wrapper.sh"]