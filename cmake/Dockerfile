FROM ubuntu:14.04
MAINTAINER John Vivian, jtvivian@gmail.com

# install dependencies first
RUN apt-get update  && apt-get install -y \
        wget \
        build-essential

# Install cmake 3.9.1
RUN wget https://cmake.org/files/v3.9/cmake-3.9.1.tar.gz && tar -xzvf cmake-3.9.1.tar.gz
RUN cd /cmake-3.9.1 && ./bootstrap && make -j4 && make install && rm -rf /cmake*

# Boilerplate
RUN mkdir /data
WORKDIR /data
ENTRYPOINT ["cmake"]
