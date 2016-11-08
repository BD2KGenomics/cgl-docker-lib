FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y curl bzip2 perl

# pull down bwa-kit
RUN curl -L http://sourceforge.net/projects/bio-bwa/files/bwakit/bwakit-0.7.12_x64-linux.tar.bz2 \
    | tar -xjC /opt/ 

# Remove this patch once the PR against bwa is merged:
# https://github.com/lh3/bwa/pull/96
ADD run-bwamem /opt/bwa.kit/run-bwamem 

# add wrapper script
ADD wrapper.sh /opt/wrapper.sh

RUN mkdir /data
WORKDIR /data

# set entrypoint to bwakit
ENTRYPOINT ["/opt/wrapper.sh"]
