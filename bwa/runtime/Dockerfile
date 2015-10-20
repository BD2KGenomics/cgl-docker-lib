FROM ubuntu:12.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN mkdir /opt/bwa/

COPY bwa /usr/local/bin/
COPY wrapper.sh /opt/bwa/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/bwa/wrapper.sh"]
