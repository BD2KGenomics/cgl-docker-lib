FROM ubuntu

MAINTAINER Audrey Musselman-Brown almussel@ucsc.edu

RUN apt-get update && \
  apt-get install -y \
    python \
    libnss3 \
    openjdk-8-jre-headless

# add spark to path
RUN mkdir /opt/apache-spark
COPY apache-spark/spark-1.5.2-bin-custom-spark.tgz /opt/
RUN tar --strip-components=1 -xzf /opt/spark-1.5.2-bin-custom-spark.tgz -C /opt/apache-spark
ENV PATH /opt/apache-spark/bin:$PATH
