FROM ubuntu:14.04

RUN apt-get update && apt-get install -y build-essential \
                   python-dev  \
                   python-pip \
                   git \
                   wget \
                   autoconf \
                   zlib1g-dev

# Make a working directory
RUN mkdir /opt/cgl-docker-lib

# Clone platypus
WORKDIR /opt/cgl-docker-lib
RUN git clone https://github.com/andyrimmer/Platypus.git

# Install htslib
RUN wget https://github.com/samtools/htslib/releases/download/1.3/htslib-1.3.tar.bz2
RUN tar xjf htslib-1.3.tar.bz2
RUN cd htslib-1.3 && autoconf && ./configure && make && make install

# Install Cython
RUN pip install cython

ENV C_INCLUDE_PATH /usr/local/include
ENV LIBRARY_PATH /usr/local/lib
ENV LD_LIBRARY_PATH /usr/local/lib

# Compile
WORKDIR /opt/cgl-docker-lib/Platypus
RUN git checkout cbbd9146183a2aba5f4884df36fbd58988133150
RUN make

ENTRYPOINT ["python", "/opt/cgl-docker-lib/Platypus/bin/Platypus.py"]