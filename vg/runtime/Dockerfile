FROM ubuntu:15.10

MAINTAINER Charles Markello, cmarkell@ucsc.edu

RUN mkdir /opt/vg/
WORKDIR /home/vg/bin
COPY vg /usr/local/bin/
WORKDIR /home/vg
COPY wrapper.sh /opt/vg/
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/vg/wrapper.sh"]
