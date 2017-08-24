FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone cannoli
RUN git clone https://github.com/bigdatagenomics/cannoli.git

# build cannoli
WORKDIR /home/cannoli
RUN git checkout 122ead2219b987bb60e5f108a2d261e056abc86e
RUN ./scripts/move_to_spark_2.sh
RUN ./scripts/move_to_scala_2.11.sh

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
