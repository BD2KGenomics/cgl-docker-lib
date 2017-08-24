FROM quay.io/ucsc_cgl/apache-hadoop-common:2.6.2

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# copy jar
COPY cannoli /opt/cgl-docker-lib/cannoli

# copy spark
COPY apache-spark /opt/cgl-docker-lib/apache-spark
ENV SPARK_HOME /opt/cgl-docker-lib/apache-spark

ENTRYPOINT ["/opt/cgl-docker-lib/cannoli/bin/cannoli-submit"]
