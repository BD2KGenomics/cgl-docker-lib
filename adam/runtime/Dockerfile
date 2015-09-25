FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# install jdk-7
RUN apt-get update
RUN apt-get install -y openjdk-7-jdk

# copy jar
RUN mkdir /opt/cgl-docker-lib
COPY adam /opt/cgl-docker-lib/adam

# copy spark
COPY apache-spark /opt/cgl-docker-lib/apache-spark
ENV SPARK_HOME /opt/cgl-docker-lib/apache-spark

CMD "/opt/cgl-docker-lib/adam/bin/adam-submit"