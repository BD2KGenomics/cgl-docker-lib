# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER Frank Austin Nothaft, fnothaft@alumni.stanford.edu

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

ENV ZIP=bcftools-1.5.tar.bz2
ENV URL=https://github.com/samtools/bcftools/releases/download/1.5/
ENV FOLDER=bcftools-1.5
ENV DST=/tmp

RUN wget $URL/$ZIP -O $DST/$ZIP && \
    tar xvf $DST/$ZIP -C $DST && \
    rm $DST/$ZIP && \
    cd $DST/$FOLDER && \
    make && \
    make install && \
    cd / && \
    rm -rf $DST/$FOLDER

RUN mkdir /opt/bcftools
COPY wrapper.sh /opt/bcftools/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/bcftools/wrapper.sh"]
