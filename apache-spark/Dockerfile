FROM ubuntu

MAINTAINER John Vivian, jtvivian@gmail.com

RUN apt-get update && \
  apt-get install -y python libnss3 openjdk-7-jre-headless curl

RUN mkdir /opt/apache-spark && \
  curl http://apache.osuosl.org/spark/spark-1.5.0/spark-1.5.0-bin-hadoop2.6.tgz \
  | tar --strip-components=1 -xzC /opt/apache-spark

ENV PATH /opt/apache-spark/bin:$PATH

RUN mkdir /data
WORKDIR /data

ENTRYPOINT ["spark-submit"]
