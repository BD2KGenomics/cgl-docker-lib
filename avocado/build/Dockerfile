FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone avocado
RUN git clone https://github.com/bigdatagenomics/avocado.git

# build avocado
WORKDIR /home/avocado
RUN ./scripts/move_to_spark_2.sh
RUN ./scripts/move_to_scala_2.11.sh

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
