FROM ubuntu:14.04

RUN apt-get update && apt-get install -y build-essential \
                   git \
                   wget \
                   autoconf \
                   zlib1g-dev \
		   cmake \
		   python-dev

# Make a working directory
RUN mkdir /opt/cgl-docker-lib

# Clone freebayes
WORKDIR /opt/cgl-docker-lib
RUN git clone https://github.com/ekg/freebayes.git --recursive

# Compile
WORKDIR /opt/cgl-docker-lib/freebayes
RUN git checkout v1.1.0
RUN git submodule update --recursive
RUN make

ENTRYPOINT ["/opt/cgl-docker-lib/freebayes/bin/freebayes"]
