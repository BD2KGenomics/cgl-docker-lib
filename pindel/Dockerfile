FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y \
        wget \
        git \
        build-essential \
        zlib1g-dev \
        ncurses-dev \
        g++ \
        python-dev

RUN mkdir /opt/pindel && mkdir /opt/samtools

WORKDIR /opt/samtools
RUN wget https://github.com/samtools/samtools/releases/download/1.2/samtools-1.2.tar.bz2
RUN tar xvjf samtools-1.2.tar.bz2
RUN cd /opt/samtools/samtools-1.2 && make && make install

WORKDIR /opt/pindel
RUN git clone https://github.com/genome/pindel.git
RUN cd pindel && git checkout v0.2.5b6
RUN cd pindel && ./INSTALL /opt/samtools/samtools-1.2/htslib-1.2.1
RUN cp /opt/pindel/pindel/pindel* /usr/local/bin/

COPY wrapper.sh /opt/pindel/
RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/pindel/wrapper.sh"]