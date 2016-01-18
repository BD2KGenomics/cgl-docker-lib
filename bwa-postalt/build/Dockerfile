FROM quay.io/ucsc_cgl/bwa-build:0.7.12

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get install -y subversion python2.7 libpthread-stubs0-dev

WORKDIR /home

# clone k8
WORKDIR /home
RUN git clone https://github.com/attractivechaos/k8.git
WORKDIR /home/k8

# clone v8
RUN git clone https://github.com/v8/v8
WORKDIR /home/k8/v8
RUN git checkout 3.16.4

# build v8
RUN make dependencies
RUN make x64.release

# now build k8
WORKDIR /home/k8
RUN g++ -O2 -Wall -o k8 -Iv8/include k8.cc -lpthread -pthread -lz /home/k8/v8/out/x64.release/obj.target/tools/gyp/libv8_base.a /home/k8/v8/out/x64.release/obj.target/tools/gyp/libv8_snapshot.a