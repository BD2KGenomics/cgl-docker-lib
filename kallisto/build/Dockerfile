FROM ubuntu:12.04

MAINTAINER Aashish Jain, 17AashishJ@students.harker.org

RUN apt-get update -y && apt-get install -y \
	cmake \
	zlib1g-dev \
	libhdf5-dev \
	git \
	build-essential

#Create new source directory
WORKDIR /home
RUN mkdir kallisto-src
WORKDIR /home/kallisto-src

#Get kallisto src
RUN git clone https://github.com/pachterlab/kallisto.git

#building kallisto
WORKDIR /home/kallisto-src/kallisto
RUN mkdir build
WORKDIR /home/kallisto-src/kallisto/build
RUN cmake ..
RUN make
RUN make install

#Moving binary
RUN mv /usr/local/bin/kallisto /home

WORKDIR /home
RUN rm -rf kallisto-src

