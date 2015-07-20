FROM ubuntu

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y picard-tools

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["picard-tools"]
