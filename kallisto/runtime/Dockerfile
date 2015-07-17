FROM ubuntu

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update && apt-get install -y libhdf5-dev

RUN mkdir /opt/cgl-docker-lib
ADD kallisto /
RUN cp kallisto /usr/bin
RUN mv kallisto /opt/cgl-docker-lib

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["kallisto"]