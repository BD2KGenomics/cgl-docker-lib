FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
        build-essential \
        zlib1g-dev \
        libncurses-dev \
        curl \
        perl-doc

RUN mkdir /opt/rsem
COPY wrapper.sh /opt/rsem/
WORKDIR /opt/rsem

RUN curl --location https://github.com/deweylab/RSEM/archive/v1.2.25.tar.gz 2> /dev/null > RSEM-1.2.25.tar.gz
RUN tar -zxvf RSEM-1.2.25.tar.gz
WORKDIR RSEM-1.2.25
RUN make

RUN mkdir /data
WORKDIR /data

ENV PATH /opt/rsem/RSEM-1.2.25:$PATH

ENTRYPOINT ["sh", "/opt/rsem/wrapper.sh"]
CMD ["--help"]