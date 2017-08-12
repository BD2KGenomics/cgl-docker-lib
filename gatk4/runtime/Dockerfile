FROM quay.io/ucsc_cgl/apache-hadoop-common:2.6.2

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

RUN apt-get update && apt-get install -y zip

# copy jar
RUN mkdir /opt/cgl-docker-lib
COPY gatk.zip /opt/cgl-docker-lib/gatk.zip
WORKDIR /opt/cgl-docker-lib/
RUN unzip gatk.zip
RUN rm -f gatk.zip

# copy spark
COPY apache-spark /opt/cgl-docker-lib/apache-spark
ENV SPARK_HOME /opt/cgl-docker-lib/apache-spark

ENTRYPOINT ["/opt/cgl-docker-lib/gatk-4.beta.3-36-gc655fef-SNAPSHOT/gatk-launch"]
