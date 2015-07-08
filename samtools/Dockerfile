FROM ubuntu

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y samtools

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["samtools"]

