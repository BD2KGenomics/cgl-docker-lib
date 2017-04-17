FROM ubuntu

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && apt-get install -y build-essential git wget

WORKDIR /home

RUN git clone https://github.com/lh3/bwa.git

WORKDIR /home/bwa

RUN wget http://zlib.net/zlib-1.2.11.tar.gz
RUN tar xvzf zlib-1.2.11.tar.gz

WORKDIR /home/bwa/zlib-1.2.11
RUN ./configure
RUN make

WORKDIR /home/bwa

RUN git checkout Apache2
RUN sed -e's#INCLUDES=#INCLUDES=-Izlib-1.2.11/ #' -e's#-lz#zlib-1.2.11/libz.a#' Makefile > Makefile.zlib
RUN make -f Makefile.zlib
