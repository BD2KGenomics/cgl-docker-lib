FROM quay.io/ucsc_cgl/apache-hadoop-common:2.6.2

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# copy jar
RUN mkdir /opt/cgl-docker-lib
COPY adam /opt/cgl-docker-lib/adam

# copy spark
COPY apache-spark /opt/cgl-docker-lib/apache-spark
ENV SPARK_HOME /opt/cgl-docker-lib/apache-spark

ENTRYPOINT ["/opt/cgl-docker-lib/adam/bin/adam-submit"]
