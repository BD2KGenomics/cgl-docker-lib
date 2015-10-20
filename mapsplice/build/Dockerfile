FROM ubuntu:12.04

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update && apt-get install -y \
	wget \
	make \
	g++ \
	unzip \
	zlib1g-dev \
	libncurses5-dev \
	python

RUN wget http://protocols.netlab.uky.edu/~zeng/MapSplice-v2.1.8.zip

RUN unzip MapSplice-v2.1.8.zip

WORKDIR /MapSplice-v2.1.8

RUN make

WORKDIR /

RUN rm MapSplice-v2.1.8.zip


