FROM ubuntu:14.04

MAINTAINER John Vivian, jtvivian@gmail.com

ENV PATH $HOME/bin:$PATH

RUN apt-get update -y && apt-get install -y \
	zlib1g-dev \
	libhdf5-serial-dev \
	git \
	build-essential \
	cmake \
	g++

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
