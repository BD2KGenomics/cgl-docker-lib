FROM ubuntu

MAINTAINER Audrey Musselman-Brown almussel@ucsc.edu

RUN apt-get update && \
  apt-get install -y \
    python \
    libnss3 \
    openjdk-8-jre-headless \
    curl

COPY download.sh /home/
RUN sh /home/download.sh

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre" >> /opt/apache-spark/conf/spark-env.sh

# add spark to path
ENV PATH /opt/apache-spark/bin:$PATH
