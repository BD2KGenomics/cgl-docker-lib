FROM ubuntu:12.04

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y build-essential zlib1g-dev git

WORKDIR /home
RUN git clone https://github.com/lh3/bwa.git

WORKDIR /home/bwa

RUN make
