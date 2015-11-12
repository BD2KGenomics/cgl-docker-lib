# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER John Vivian, jtvivian@gmail.com
# Original Author: Saulo Alves Aflitos <sauloal@gmail.com>

################## BEGIN INSTALLATION ######################
RUN apt-get update && \
    apt-get install -y \
      libncurses5-dev \
      libncursesw5-dev \
      build-essential \
      zlib1g-dev \
      wget && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ENV ZIP=samtools-1.2.tar.bz2
ENV URL=https://github.com/BioDocker/software-archive/releases/download/samtools
ENV FOLDER=samtools-1.2
ENV DST=/tmp

RUN wget $URL/$ZIP -O $DST/$ZIP && \
    tar xvf $DST/$ZIP -C $DST && \
    rm $DST/$ZIP && \
    cd $DST/$FOLDER && \
    make && \
    make install && \
    cd / && \
    rm -rf $DST/$FOLDER

# File Author / Maintainer
MAINTAINER Saulo Alves Aflitos <sauloal@gmail.com>

RUN mkdir /opt/samtools
COPY wrapper.sh /opt/samtools/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/samtools/wrapper.sh"]
