FROM quay.io/ucsc_cgl/cmake:3.9.1
MAINTAINER John Vivian, jtvivian@gmail.com

# install dependencies first
RUN apt-get update  && apt-get install -y \
		build-essential \
		liblzma-dev \
		libbz2-dev \
		libz-dev \
		git \
		wget

# install hera from source
WORKDIR /
RUN git clone https://github.com/bioturing/hera.git
WORKDIR /hera
RUN git checkout 53dd2a1927d86d2299f16cf265d3f0e259c0e3df
RUN chmod +x build.sh
RUN ./build.sh

# Boilerplate
RUN mkdir -p /data
WORKDIR /data
ENTRYPOINT ["/hera/build/hera"]
