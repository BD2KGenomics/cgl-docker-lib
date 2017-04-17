FROM quay.io/ucsc_cgl/spark-and-maven:2.1.0.3.3.9

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# clone conductor
WORKDIR /home
RUN git clone https://github.com/BD2KGenomics/conductor.git

# build conductor
WORKDIR /home/conductor
RUN /opt/apache-maven-3.3.9/bin/mvn package \
    -DskipTests \
    -Dhadoop.version=2.6.0 \
    -Dspark.version=1.5.2
