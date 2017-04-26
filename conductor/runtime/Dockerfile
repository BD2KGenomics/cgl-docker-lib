FROM ubuntu

MAINTAINER Frank Austin Nothaft, fnothaft@berkeley.edu

# install jdk-7
RUN apt-get update && apt-get install -y openjdk-8-jdk

# copy jar
RUN mkdir /opt/cgl-docker-lib
COPY conductor /opt/cgl-docker-lib/conductor

# copy spark
COPY apache-spark /opt/cgl-docker-lib/apache-spark
ENV SPARK_HOME /opt/cgl-docker-lib/apache-spark

# copy entry script
COPY wrapper.sh /opt/cgl-docker-lib/wrapper.sh

ENTRYPOINT ["bash", "/opt/cgl-docker-lib/wrapper.sh"]
