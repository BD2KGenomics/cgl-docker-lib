FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone cannoli
RUN git clone https://github.com/bigdatagenomics/cannoli.git

# build cannoli
WORKDIR /home/cannoli
RUN git checkout 4395e5b2e6040cbe5a24398d87ae49535fa62a23

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
