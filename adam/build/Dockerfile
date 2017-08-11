FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone adam
RUN git clone https://github.com/bigdatagenomics/adam.git

# build adam
WORKDIR /home/adam
RUN git checkout c251f79c6bde3dce12e685c6cf03d5b1c30e9273

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests -Dspark.version=1.6.3
