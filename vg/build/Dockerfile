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
RUN git checkout ea8edfd613f151954daea9fdb66901553265a509
RUN git submodule update --init --recursive
RUN make get-deps

# Build vg 
RUN ./source_me.sh && make static
