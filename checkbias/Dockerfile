# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER John Vivian <jtvivian@gmail.com>

# Update the repository sources list
RUN sudo apt-get update && sudo apt-get install --yes \
        build-essential \
        git \
        python-pip \
        python-dev \
        zlib1g-dev \
        python-numpy \
        python-scipy \
        python-matplotlib

RUN pip install --upgrade pip
RUN pip install pysam pandas

# Download checkbias
RUN mkdir /data
RUN git clone https://github.com/KjongLehmann/m53/ /opt/checkbias
RUN cd /opt/checkbias && git checkout 612f1296541cb76622d8f8b5df7d9072417bd3ac

# CGL Boilerplate
COPY wrapper.sh /opt/checkbias/
WORKDIR /data

ENTRYPOINT ["sh", "/opt/checkbias/wrapper.sh"]
