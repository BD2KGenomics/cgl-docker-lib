FROM ubuntu

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update && apt-get install -y \
	zlib1g-dev \
	git \
	make

RUN git clone https://github.com/lh3/bwa.git

RUN cd bwa; make
WORKDIR /bwa