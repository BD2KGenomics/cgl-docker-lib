FROM ubuntu:14.04

RUN apt-get update && \
  apt-get install -y python libnss3 curl

# Download Manta binary
RUN mkdir /opt/manta && \
  curl -L https://github.com/Illumina/manta/releases/download/v1.1.1/manta-1.1.1.centos5_x86_64.tar.bz2 \
  | tar --strip-components=1 -xjC /opt/manta
