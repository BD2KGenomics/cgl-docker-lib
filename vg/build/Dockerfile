FROM ubuntu:15.10

MAINTAINER Charles Markello, cmarkell@ucsc.edu

# Install vg dependencies
RUN apt-get update \
	&& apt-get install -y \
		build-essential \
		gcc-4.9 \
		g++-4.9 \
		pkg-config \
		sudo \
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
RUN git checkout 8a28f7df06989342c89fa0e9c729db64257188ba
RUN make get-deps

# Build vg 
RUN . ./source_me.sh && make static
