FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

WORKDIR /home

# clone adam
RUN git clone https://github.com/bigdatagenomics/adam.git

ENV MAVEN_OPTS "-Xmx2g"

# build adam
WORKDIR /home/adam
RUN git checkout 50d29af4a65d51f6db75361e1ddf32c12a9e149a
RUN ./scripts/move_to_spark_2.sh
RUN ./scripts/move_to_scala_2.11.sh

RUN /opt/apache-maven-3.3.9/bin/mvn package -DskipTests
