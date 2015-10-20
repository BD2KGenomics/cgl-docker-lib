FROM ubuntu:12.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y picard-tools man

RUN mkdir /opt/picard-tools
COPY wrapper.sh /opt/picard-tools/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/picard-tools/wrapper.sh"]
CMD ["--help"]