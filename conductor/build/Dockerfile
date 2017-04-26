FROM quay.io/ucsc_cgl/spark-and-maven

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# clone conductor
WORKDIR /home
RUN git clone https://github.com/fnothaft/conductor.git

# build conductor
WORKDIR /home/conductor
RUN git checkout issues/19-scala-spark-cross-build
RUN scripts/move_to_spark_2.sh
RUN /opt/apache-maven-3.3.9/bin/mvn package \
    -DskipTests \
    -Dhadoop.version=2.6.0 \
    -Dspark.version=1.5.2
