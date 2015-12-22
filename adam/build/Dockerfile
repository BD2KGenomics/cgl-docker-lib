FROM computationalgenomicslab/spark-and-maven:1.5.2.3.3.3-build

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone adam
RUN git clone https://github.com/bigdatagenomics/adam.git

# build adam
WORKDIR /home/adam
RUN /opt/apache-maven-3.3.3/bin/mvn package -DskipTests
