FROM ubuntu

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update && apt-get install -y libhdf5-dev

ADD kallisto /
RUN mv kallisto /usr/local/bin

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["kallisto"]