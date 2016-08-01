FROM quay.io/ucsc_cgl/spark-and-maven:1.5.2.3.3.9

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone quinine
RUN git clone https://github.com/bigdatagenomics/quinine.git

# build quinine
WORKDIR /home/quinine
RUN git checkout 2475aea0f800ce293dbf18e743c500a0cd51e403

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
