# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER Sophie Lemoine <slemoine@biologie.ens.fr>

# Update the repository sources list
RUN apt-get update && apt-get install --yes \
    build-essential \
    gcc-multilib \
    apt-utils \
    zlib1g-dev \
    vim-common \
    git \
    wget

# Compile and install STAR
WORKDIR /tmp 
RUN wget https://github.com/alexdobin/STAR/archive/2.5.3a.tar.gz
RUN tar -xzf 2.5.3a.tar.gz
WORKDIR /tmp/STAR-2.5.3a/source
RUN make STAR 
RUN mv STAR /usr/local/bin/

# Cleanup                                                                                                                                                                                                                                                                                                             
RUN rm -rf /tmp/STAR
RUN apt-get clean
RUN apt-get remove --yes --purge build-essential gcc-multilib apt-utils zlib1g-dev vim-common git

# CGL Boilerplate
RUN mkdir /opt/star
COPY wrapper.sh /opt/star/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/star/wrapper.sh"]
