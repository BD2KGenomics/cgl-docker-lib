# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && \
    apt-get install -y \
      libncurses5-dev \
      libncursesw5-dev \
      build-essential \
      zlib1g-dev \
      libbz2-dev \
      liblzma-dev \
      wget && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV ZIP=samtools-1.8.tar.bz2
ENV URL=https://github.com/samtools/samtools/releases/download/1.8/
ENV FOLDER=samtools-1.8
ENV DST=/tmp

RUN wget $URL/$ZIP -O $DST/$ZIP && \
    tar xvf $DST/$ZIP -C $DST && \
    rm $DST/$ZIP && \
    cd $DST/$FOLDER && \
    make && \
    make install && \
    cd / && \
    rm -rf $DST/$FOLDER

RUN mkdir /opt/samtools
COPY wrapper.sh /opt/samtools/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/samtools/wrapper.sh"]
