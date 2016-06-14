FROM ubuntu:15.10

MAINTAINER Charles Markello, cmarkell@ucsc.edu

RUN apt-get update \
	&& apt-get update && apt-get install -y \
	gcc-4.9 \
	g++-4.9 \
	git \
	make \
	protobuf-compiler \
	libprotoc-dev \
	libjansson-dev \
	libbz2-dev \
	libncurses5-dev \
	automake libtool jq samtools curl unzip redland-utils \
	librdf-dev cmake pkg-config wget bc gtk-doc-tools raptor2-utils rasqal-utils bison flex

WORKDIR /home
RUN git clone --recursive https://github.com/vgteam/vg.git

WORKDIR /home/vg

RUN ./source_me.sh && make static
