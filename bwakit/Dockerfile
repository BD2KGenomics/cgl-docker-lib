FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y curl bzip2 perl make g++

# pull down bwa-kit
RUN curl -L http://sourceforge.net/projects/bio-bwa/files/bwakit/bwakit-0.7.15_x64-linux.tar.bz2 \
    | tar -xjC /opt/

# get latest version of samblaster and build
RUN curl -L https://github.com/GregoryFaust/samblaster/releases/download/v.0.1.24/samblaster-v.0.1.24.tar.gz \
    | tar -xvz -C /opt/ \
    && cd /opt/samblaster-v.0.1.24 \
    && make

# Remove this patch once the PR against bwa is merged:
# https://github.com/lh3/bwa/pull/96
ADD run-bwamem /opt/bwa.kit/run-bwamem 

# add wrapper script
ADD wrapper.sh /opt/wrapper.sh

RUN mkdir /data
WORKDIR /data

# set entrypoint to bwakit
ENTRYPOINT ["/opt/wrapper.sh"]
