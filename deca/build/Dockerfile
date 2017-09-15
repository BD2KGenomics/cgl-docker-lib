FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone deca
WORKDIR /home/
RUN git clone https://github.com/bigdatagenomics/deca.git

# build deca
WORKDIR /home/deca
RUN git checkout deca-parent-0.1.0

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
