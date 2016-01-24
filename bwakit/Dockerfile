FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && \
  apt-get install -y \
    curl

# pull down bwa-kit
RUN curl -L http://sourceforge.net/projects/bio-bwa/files/bwakit/bwakit-0.7.12_x64-linux.tar.bz2 \
  | tar -xjC /opt/

# add wrapper script
ADD wrapper.sh /opt/wrapper.sh

# set entrypoint to bwakit
ENTRYPOINT ["/opt/wrapper.sh"]