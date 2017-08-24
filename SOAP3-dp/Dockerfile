FROM ubuntu:14.04

RUN apt-get update && apt-get install -y build-essential zlib1g-dev git

# Make a working directory
RUN mkdir /opt/cgl-docker-lib

# Clone SOAP3-dp
WORKDIR /opt/cgl-docker-lib
RUN git clone https://github.com/aquaskyline/SOAP3-dp.git

# Compile
WORKDIR /opt/cgl-docker-lib/SOAP3-dp
RUN git checkout 8814dcd4958b24c68b46772f790f5477644c5cc3
RUN make SOAP3-Builder
RUN make BGS-Build