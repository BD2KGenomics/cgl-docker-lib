FROM quay.io/ucsc_cgl/spark-and-maven:1.5.2.3.3.9

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone quinine
RUN git clone https://github.com/bigdatagenomics/quinine.git

# build quinine
WORKDIR /home/quinine
RUN git checkout a987006fdf38afadc9c6a22061885f8e105234f7

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
