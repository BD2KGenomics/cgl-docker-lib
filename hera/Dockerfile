FROM quay.io/ucsc_cgl/cmake:3.9.1
MAINTAINER John Vivian, jtvivian@gmail.com

# install dependencies first
RUN apt-get update  && apt-get install -y \
		build-essential \
		liblzma-dev \
		libbz2-dev \
		libz-dev \
		git \
		wget \
		python

# install hera from source
WORKDIR /
RUN git clone https://github.com/bioturing/hera.git
WORKDIR /hera
RUN git checkout tags/hera-v1.1
RUN chmod +x build.sh
RUN ./build.sh

# Fix missing import in hera_build
RUN awk 'NR==2 {print "import os"} 1' /hera/build/hera_build > /hera/build/foo
RUN mv /hera/build/foo /hera/build/hera_build; chmod +x /hera/build/hera_build

# Boilerplate
RUN mkdir -p /data
WORKDIR /data
ENTRYPOINT ["/hera/build/hera"]
