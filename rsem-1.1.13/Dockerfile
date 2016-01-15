FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
        build-essential \
        zlib1g-dev \
        libncurses-dev \
        curl \
        perl-doc \
        libswitch-perl

RUN mkdir /opt/rsem
COPY wrapper.sh /opt/rsem/
WORKDIR /opt/rsem

RUN curl --location http://deweylab.biostat.wisc.edu/rsem/src/rsem-1.1.13.tar.gz 2> /dev/null > rsem-1.1.13.tar.gz
RUN tar -zxvf rsem-1.1.13.tar.gz
WORKDIR rsem-1.1.13
RUN make

RUN mkdir /data
WORKDIR /data

ENV PATH /opt/rsem/rsem-1.1.13:$PATH

ENTRYPOINT ["sh", "/opt/rsem/wrapper.sh"]
CMD ["--help"]