FROM ubuntu:12.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y samtools

RUN mkdir /opt/samtools
COPY wrapper.sh /opt/samtools/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/samtools/wrapper.sh"]
