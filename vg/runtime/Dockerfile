FROM ubuntu:14.04

MAINTAINER Charles Markello, cmarkell@ucsc.edu

RUN mkdir /opt/vg/

RUN pwd
RUN ls -l
WORKDIR /home/vg/bin
RUN pwd
RUN ls -l
COPY vg /usr/local/bin/
RUN pwd
RUN ls -l
WORKDIR /home/vg
RUN pwd
RUN ls -l
COPY wrapper.sh /opt/vg/
RUN pwd
RUN ls -l

RUN mkdir /data
RUN pwd
RUN ls -l
WORKDIR /data
RUN pwd
RUN ls -l

ENTRYPOINT ["sh", "/opt/vg/wrapper.sh"]
