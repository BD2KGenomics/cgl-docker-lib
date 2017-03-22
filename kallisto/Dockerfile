FROM ubuntu:14.04
MAINTAINER John Vivian, jtvivian@gmail.com

# Original Author: insilicodb: https://hub.docker.com/r/insilicodb/kallisto/

# install dependencies first
RUN apt-get update  && apt-get install -y \
		build-essential \
		cmake \
		python \
		python-pip \
		python-dev \
		hdf5-tools \
		libhdf5-dev \
		hdf5-helpers \
		libhdf5-serial-dev \
		git \
		apt-utils

# install kallisto from source
WORKDIR /docker
RUN git clone https://github.com/pachterlab/kallisto.git
WORKDIR /docker/kallisto
RUN git checkout 1e0e11288558ad88af198ec4f5302129c249b44f
RUN mkdir build
WORKDIR /docker/kallisto/build
RUN cmake .. && \
	make && \
	make install

RUN mkdir /opt/kallisto
COPY wrapper.sh /opt/kallisto/

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["sh", "/opt/kallisto/wrapper.sh"]
